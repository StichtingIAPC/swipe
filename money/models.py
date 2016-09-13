from decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models

# Based on https://git.iapc.utwente.nl/swipe/swipe-design/issues/22
# Global money representation parameters

from django.utils.translation import ugettext_lazy

from swipe.settings import DECIMAL_PLACES, MAX_DIGITS, USED_CURRENCY


# VAT : Pay the government, alas, we have to do this.
from tools.util import _assert


class VAT(models.Model):
    # What's the Rate of this VAT (percentage)? This is the multiplication factor.
    vatrate = models.DecimalField(decimal_places=6, max_digits=8)
    # What's this VAT level called?
    name = models.CharField(max_length=255)
    # Is this VAT level in use?
    active = models.BooleanField()

    def __str__(self):
        return "{}:{}".format(self.name, self.vatrate)

    def to_rate_string(self):
        return "{}%".format((self.rate - 1) * 100)


class AccountingGroup(models.Model):
    # Number for internal administration
    accounting_number = models.IntegerField()
    # Vat group
    vat_group = models.ForeignKey(VAT)
    # Group name
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}({})".format(self.name,self.vat_group.to_rate_string())


class VATLevelField(models.DecimalField):
    description = "VAT level, in rate, not in percentage."

    def __init__(self, *args, **kwargs):
        kwargs['decimal_places'] = 6
        kwargs['max_digits'] = 15

        super(VATLevelField, self).__init__(*args, **kwargs)


# Currency describes the currency of a monetary value. It's also used to describe the currency used in a till
class Currency:
    def __init__(self, iso: str):
        _assert(len(iso) == 3), "Valid ISO currency codes are exactly three characters long, given {}".format(iso)
        self._iso = iso

    @property
    def iso(self):
        return self._iso

    def __str__(self):
        return self.iso

    def __eq__(self, oth):
        return oth is not None and self.iso == oth.iso


def currency_field_name(name):
    return "{}_currency".format(name)


def vat_field_name(name):
    return "{}_vat".format(name)


def cost_field_name(name):
    return "{}_cost".format(name)


def price_field_name(name):
    return "{}_price".format(name)


class Money:
    def __init__(self, amount, currency=None, use_system_currency=False):
        if use_system_currency:
            currency = Currency(iso=USED_CURRENCY)
        self._amount = amount.quantize(Decimal(10)**(-DECIMAL_PLACES))
        self._currency = currency

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def __eq__(self, oth):
        return type(oth) == Money and self.amount == oth.amount and self.currency == oth.currency

    def __str__(self):
        return "{}: {}".format(self.currency.iso, self._amount)

    def compare(self, item2):
        if type(self) != type(item2):
            raise TypeError("Cannot compare objects of type {} and {}".format(type(self), type(item2)))
        else:
            return self == item2

    def __add__(self, oth):
        if type(oth) != Money:
            raise TypeError("Cannot add Money to {}".format(type(oth)))
        if oth.currency == self.currency:
            return Money(self.amount + oth.amount, self.currency)
        else:
            raise TypeError("Trying to add different currencies")

    def __sub__(self, oth):
        if type(oth) != Money:
            raise TypeError("Cannot subtract Money from ".format(type(oth)))
        if oth.currency == self.currency:
            return Money(self.amount - oth.amount, self.currency)
        else:
            raise TypeError("Trying to subtract different currencies")

    def __mul__(self, oth):
        if isinstance(oth, int) or isinstance(oth, float) or isinstance(oth, Decimal):
            return Money(self.amount * oth, self.currency)
        else:
            raise TypeError("Cannot multiply Money with {}".format(type(oth)))

    def __truediv__(self, oth):
        if isinstance(oth, int):
            return Money(self.amount / Decimal(oth), self.currency)
        else:
            raise TypeError("Cannot divide Money by {}".format(type(oth)))


class MoneyProxy:
    # sets the correct column names for this field.
    def __init__(self, field, name, money_type):
        self.field = field
        self.amount_field_name = name
        self.type = money_type
        self.currency_field_name = currency_field_name(name)

    def _get_values(self, obj):
        return (obj.__dict__.get(self.amount_field_name, None),
                obj.__dict__.get(self.currency_field_name, None))

    def _set_values(self, obj, amount, currency):
        obj.__dict__[self.amount_field_name] = amount
        obj.__dict__[self.currency_field_name] = currency

    # noinspection PyUnusedLocal
    def __get__(self, obj, *args):
        amount, currency = self._get_values(obj)
        if amount is None:
            return None

        return money_types[self.type](amount, Currency(currency))

    def __set__(self, obj, value):
        if value is None:  # Money(0) is False
            self._set_values(obj, None, '')
        elif isinstance(value, money_types[self.type]):
            self._set_values(obj, value.amount, value.currency.iso)
        else:
            amount = Decimal(str(value))
            _, currency = self._get_values(obj)  # use what is currently set
            self._set_values(obj, amount, currency)


class CurrencyField(models.CharField):
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value


# Money describes a monetary value. It would be used to describe both cost and price values.
# Generally Money itself isn't used in business logic, instead, price and cost are used.
# This is intended as a 'smart'  version of a decimal, but in most cases you should look at Price, CostPrice or Cost,
# these are the droids you are looking for (In models: PriceField, CostPriceField, CostField).
class MoneyField(models.DecimalField):
    description = ugettext_lazy('An amount and type of currency')

    def __init__(self, *args, **kwargs):

        kwargs['decimal_places'] = DECIMAL_PLACES
        kwargs['max_digits'] = MAX_DIGITS
        self.type = kwargs.pop('type', "money")

        self.add_currency_field = not kwargs.pop('no_currency_field', False)
        super(MoneyField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MoneyField, self).deconstruct()
        kwargs['no_currency_field'] = True
        return name, path, args, kwargs

    # currency: Which currency is this money in?
    def contribute_to_class(self, cls, name, virtual_only=False):
        if self.add_currency_field:
            c_field = CurrencyField(max_length=3)
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(currency_field_name(name), c_field)
        super(MoneyField, self).contribute_to_class(cls, name)
        setattr(cls, name, MoneyProxy(self, name, self.type))

    # The boiler needs some plating
    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, money_types[self.type]):
            value = value.amount

            return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if isinstance(value, money_types[self.type]):
            value = value.amount
            return super(MoneyField.get_prep_lookup(self, lookup_type, value))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.amount


# Cost describes the cost made for a certain thing.
# It could for instance describe the order cost related to a product on stock.
class Cost(Money):
    def compare(self, item2):
        if type(self) != type(item2):
            raise TypeError("Cannot compare objects of type {} and {}".format(type(self), type(item2)))
        else:
            return self == item2

    def __eq__(self, oth):
        return type(oth) == Cost and self.amount == oth.amount and self.currency == oth.currency

    def __add__(self, oth):
        if type(oth) != Cost:
            raise TypeError("Cannot add Cost to {}".format(type(oth)))

        if oth.currency == self.currency:
            return Cost(self.amount + oth.amount, self.currency)
        else:
            raise TypeError("Trying to add different currencies")

    def __sub__(self, oth):
        if type(oth) != Cost:
            raise TypeError("Cannot subtract Cost from {}".format(type(oth)))

        if oth.currency == self.currency:
            return Cost(self.amount - oth.amount, self.currency)
        else:
            raise TypeError("Trying to subtract different currencies")

    def __mul__(self, oth):
        if isinstance(oth, int):
            return Cost(self.amount * oth, self.currency)
        else:
            raise TypeError("Cannot multiply Cost with {}".format(type(oth)))

    def __truediv__(self, oth):
        if isinstance(oth, int):
            return Cost(self.amount / oth, self.currency)
        else:
            raise TypeError("Cannot divide Cost by {}".format(type(oth)))

    def __str__(self):
        return super(Cost, self).__str__()


class CostField(MoneyField):
    def __init__(self, *args, **kwargs):
        kwargs["type"] = "cost"
        super(CostField, self).__init__(*args, **kwargs)


# A price describes a monetary value which is intended to be used on the sales side
class Price(Money):
    #TODO: SAVE CHECK?``
    def __init__(self, amount, vat=None, currency=None, use_system_currency=False):
        if use_system_currency:
            currency = Currency(iso=USED_CURRENCY)
        super().__init__(amount, currency)
        self._vat = vat

    @property
    def vat(self):
        return self._vat

    def __eq__(self, other):
        return type(other) == Price and self.amount == other.amount \
               and self.currency == other.currency and self.vat == other.vat

    def compare(self, item2):
        if type(self) != type(item2):
            raise TypeError("Cannot compare objects of type {} and {}".format(type(self), type(item2)))
        else:
            return self == item2

    def __add__(self, oth):
        if type(oth) != Price:
            raise TypeError("Cannot add Price to {}".format(type(oth)))

        if oth.vat != self.vat:
            raise TypeError("VAT levels of numbers to be added are not the same. "
                            "Got {} and {}".format(oth.vat, self.vat))

        if oth.currency != self.currency:
            raise TypeError("Trying to add different currencies")

        return Price(self.amount + oth.amount, self.vat, self.currency)

    def __sub__(self, oth):
        if not isinstance(oth, Price):
            raise TypeError("Cannot subtract Price from {}".format(type(oth)))

        if oth.vat != self.vat:
            raise TypeError("VAT levels of numbers to be subtracted are not the same. "
                            "Got {} and {}".format(oth.vat, self.vat))

        if oth.currency != self.currency:
            raise TypeError("Trying to subtract different currencies")

        return Price(self.amount - oth.amount, self.vat, self.currency)

    def __mul__(self, oth):
        if isinstance(oth, int) or isinstance(oth, float) or isinstance(oth, Decimal):
            return Price(self.amount * oth, self.vat, self.currency)
        else:
            raise TypeError("Cannot multiply Price with {}".format(type(oth)))


class PriceProxy:
    # sets the correct column names for this field.
    def __init__(self, field, name, price_type):
        self.field = field
        self.amount_field_name = name
        self.type = price_type
        self.currency_field_name = currency_field_name(name)
        self.vat_field_name = vat_field_name(name)

    def _get_values(self, obj):
        return (obj.__dict__.get(self.amount_field_name, None),
                obj.__dict__.get(self.currency_field_name, None), obj.__dict__.get(self.vat_field_name, None))

    def _set_values(self, obj, amount, currency, vat):
        obj.__dict__[self.amount_field_name] = amount
        obj.__dict__[self.currency_field_name] = currency
        obj.__dict__[self.vat_field_name] = vat

    # noinspection PyUnusedLocal
    def __get__(self, obj, *args):
        amount, currency, vat = self._get_values(obj)
        if amount is None:
            return None

        return Price(amount, vat, Currency(currency))

    def __set__(self, obj, value):
        if value is None:  # Money(0) is False
            self._set_values(obj, None, '', Decimal("1.21"))
        elif isinstance(value, Price):
            self._set_values(obj, value.amount, value.currency.iso, value.vat)
        else:
            amount = Decimal(str(value))
            _, currency, vat = self._get_values(obj)  # use what is currently set
            self._set_values(obj, amount, currency, vat)


class PriceField(models.DecimalField):
    description = ugettext_lazy('An amount and type of currency')

    def __init__(self, *args, **kwargs):

        kwargs['decimal_places'] = DECIMAL_PLACES
        kwargs['max_digits'] = MAX_DIGITS
        self.type = kwargs.pop('type', "money")

        self.add_currency_field = not kwargs.pop('no_currency_field', False)
        self.add_vat_field = not kwargs.pop('no_vat_field', False)

        super(PriceField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(PriceField, self).deconstruct()
        kwargs['no_currency_field'] = True
        kwargs['no_vat_field'] = True

        return name, path, args, kwargs

    # currency: Which currency is this money in?
    def contribute_to_class(self, cls, name, virtual_only=False):
        if self.add_currency_field:
            c_field = CurrencyField(max_length=3)
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(currency_field_name(name), c_field)
        if self.add_vat_field:
            c_field = VATLevelField()
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(vat_field_name(name), c_field)
        super(PriceField, self).contribute_to_class(cls, name)
        setattr(cls, name, PriceProxy(self, name, self.type))

    # The boiler needs some plating
    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, Price):
            value = value.amount
            return super(PriceField, self).get_db_prep_save(value, *args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if isinstance(value, Price):
            value = value.amount
            return super(PriceField.get_prep_lookup(self, lookup_type, value))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.amount


class SalesPrice(Price):
    """
        The SalesPrice is the price of an object, for which a cost is known.
    """
    def __init__(self, amount, vat, currency, cost, use_system_currency=False):
        if use_system_currency:
            currency = Currency(iso=USED_CURRENCY)
        super().__init__(amount, vat, currency)
        self._cost = cost

    @property
    def cost(self):
        return self._cost

    def __eq__(self, other):
        return type(other) == SalesPrice and self.amount == other.amount and self.currency == other.currency \
               and self.vat == other.vat and self.cost == other.cost

    def __add__(self, oth):
        if type(oth) != SalesPrice:
            raise TypeError("Cannot add SalesPrice to {}".format(type(oth)))

        if oth.vat != self.vat:
            raise TypeError("VAT levels of numbers to be added are not the same. "
                            "Got {} and {}".format(oth.vat, self.vat))

        if oth.currency != self.currency:
            raise TypeError("Trying to add different currencies")

        return SalesPrice(self.amount + oth.amount, self.vat, self.currency, self.cost + oth.cost)

    def __sub__(self, oth):
        if type(oth) != SalesPrice:
            raise TypeError("Cannot subtract SalesPrice from {}".format(type(oth)))

        if oth.vat != self.vat:
            raise TypeError("VAT levels of numbers to be subtracted are not the same. "
                            "Got {} and {}".format(oth.vat, self.vat))

        if oth.currency != self.currency:
            raise TypeError("Trying to subtract different currencies")

        return SalesPrice(self.amount - oth.amount, self.vat, self.currency, self.cost - oth.cost)

    def __mul__(self, oth):
        if isinstance(oth, int) or isinstance(oth, float) or isinstance(oth, Decimal):
            return SalesPrice(self.amount * oth, self.vat, self.currency, self.cost * oth)
        else:
            raise TypeError("Cannot multiply SalesPrice with {}".format(type(oth)))

    def get_profit(self):
        return self.amount / self.vat - self.cost

    def get_margin(self):
        return self.get_profit() / self.cost

    def __str__(self):
        return "{}, Price: {}, Cost: {}".format(self.currency.iso, self.amount, self.cost)


class SalesPriceProxy:
    """
     The SalesPriceProxy is responsible for converting data from Django (SalesPriceField) to SalesPrice Objects.
    """
    def __init__(self, field, name, price_type):
        self.field = field
        self.amount_field_name = name
        self.type = price_type
        self.currency_field_name = currency_field_name(name)
        self.cost_field = cost_field_name(name)
        self.vat_field_name = vat_field_name(name)

    def _get_values(self, obj):
        return (obj.__dict__.get(self.amount_field_name, None),
                obj.__dict__.get(self.currency_field_name, None), obj.__dict__.get(self.vat_field_name, None),
                obj.__dict__.get(self.cost_field, None))

    def _set_values(self, obj, amount, currency, vat, cost):
        obj.__dict__[self.amount_field_name] = amount
        obj.__dict__[self.currency_field_name] = currency
        obj.__dict__[self.vat_field_name] = vat
        obj.__dict__[self.cost_field] = cost

    # noinspection PyUnusedLocal
    def __get__(self, obj, *args):
        amount, currency, vat, cost = self._get_values(obj)
        if amount is None:
            return None

        return SalesPrice(amount, vat, Currency(currency), cost)

    def __set__(self, obj, value):
        if value is None:  # Money(0) is False
            self._set_values(obj, None, '', Decimal("0"), Decimal("0"))
        elif isinstance(value, SalesPrice):
            self._set_values(obj, value.amount, value.currency.iso, value.vat, value.cost)
        else:

            amount = Decimal(str(value))
            _, currency, vat, cost = self._get_values(obj)  # use what is currently set
            self._set_values(obj, amount, currency, vat, cost)


class SalesPriceField(models.DecimalField):
    """
        A SalesPriceField is the Django representation of a SalesPrice. As such, it's responsible for properly
        creating the Django representation of the fields used to store a SalesPrice.
        It contains the following fields:
        currency : In what currency is this SalesPrice?
        amount : What's the amount of currency?
        vat : At what VAT is this currency?
        cost : What's the cost made for this SalePrice?
    """
    description = ugettext_lazy('An amount and type of currency')

    def __init__(self, *args, **kwargs):

        kwargs['decimal_places'] = DECIMAL_PLACES
        kwargs['max_digits'] = MAX_DIGITS
        self.type = kwargs.pop('type', "money")

        self.add_currency_field = not kwargs.pop('no_currency_field', False)
        self.add_vat_field = not kwargs.pop('no_vat_field', False)
        self.add_cost_field = not kwargs.pop("no_cost_field", False)
        super(SalesPriceField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(SalesPriceField, self).deconstruct()
        kwargs['no_currency_field'] = True
        kwargs['no_vat_field'] = True
        kwargs['no_cost_field'] = True

        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, virtual_only=False):
        if self.add_currency_field:
            c_field = CurrencyField(max_length=3)
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(currency_field_name(name), c_field)
        if self.add_vat_field:
            c_field = VATLevelField()
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(vat_field_name(name), c_field)
        if self.add_cost_field:
            c_field = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
            c_field.creation_counter = self.creation_counter
            cls.add_to_class(cost_field_name(name), c_field)
        super(SalesPriceField, self).contribute_to_class(cls, name)
        setattr(cls, name, SalesPriceProxy(self, name, self.type))

    # The boiler needs some plating
    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, SalesPrice):
            value = value.amount
            return super(SalesPriceField, self).get_db_prep_save(value, *args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if isinstance(value, SalesPrice):
            value = value.amount
            return super(SalesPriceField.get_prep_lookup(self, lookup_type, value))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.amount


class CurrencyData(models.Model):
    """
    The data necessary to retrieve amongst others currency symbols and denomination is stored in here.
    """
    # ISO4217-name
    iso = models.CharField(primary_key=True, max_length=3, unique=True,
                           validators=[RegexValidator(regex='^.{3}$', message='ISO length should be 3.')])
    # English name
    name = models.CharField(max_length=255)
    # Max digits for transaction
    digits = models.IntegerField()
    # Currency symbol
    symbol = models.CharField(max_length=5)

    def __eq__(self, other):
        if isinstance(other, CurrencyData):
            return self.iso == other.iso
        else:
            return False

    def __str__(self):
        return self.iso


class Denomination(models.Model):
    """
    The currency bundles that a currency has. A cash register can pay cash with only these means
    """
    currency = models.ForeignKey(CurrencyData)

    amount = models.DecimalField(decimal_places=DECIMAL_PLACES, max_digits=MAX_DIGITS)

    @classmethod
    def create(cls, *args, **kwargs):
        if not len(kwargs) == 2:
            raise TypeError("All arguments need to be specified")
        else:
            return cls(*args, **kwargs)

    def save(self, **kwargs):
        _assert(self.currency and self.amount)
        super(Denomination, self).save()

    def __str__(self):
        return "{} {}".format(self.currency.iso, self.amount)

    def has_same_currency(self, other):
        if isinstance(other, Denomination):
            return self.currency == other.currency
        else:
            return False

    def __eq__(self, other):
        """
        This function may be removed if different denominations with the same amount are not equal
        """
        if isinstance(other, Denomination):
            return (self.amount == other.amount) and (self.currency == other.currency)
        else:
            return False


class TestMoneyType(models.Model):
    money = MoneyField(type="money")


class TestOtherMoneyType(models.Model):
    money = MoneyField(type="money")


class TestCostType(models.Model):
    cost = MoneyField(type="cost")


class TestSalesPriceType(models.Model):
    price = SalesPriceField()


class TestPriceType(models.Model):
    price = PriceField(type="cost")


# Define monetary types here
money_types = {"cost": Cost, "money": Money}
