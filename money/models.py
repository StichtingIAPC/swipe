from decimal import Decimal
from django.db import models

# Create your models here.

# VAT : Pay the government, alas, we have to do this.
from django.utils.translation import ugettext_lazy


class VAT (models.Model):
    # What's the Rate of this VAT (percentage)? This is the multiplication factor.
    rate = models.DecimalField(decimal_places=6, max_digits=7,verbose_name="VAT Rate")
    # What's this VAT level called?
    name = models.CharField(max_length=255, verbose_name="VAT Name")
    # Is this VAT level in use?
    active = models.BooleanField()

    def to_rate_string(self):
        return ((self.rate-1)*100)+"%"


# Currency describes the currency of a monetary value. It's also used to describe the currency used in a till
class Currency:
    def __init__(self, iso: str):
        assert len(iso) == 3, "Valid ISO currency codes are exactly three characters long, given " + iso
        self._iso = iso

    @property
    def iso(self):
        return self._iso

    def __eq__(self, other):
        return other is not None and self.iso == other.iso


def currency_field_name(name):
    return "%s_currency" % name


class Money:
    def __init__(self,amount, currency):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return self.currency.iso+": "+ str(self.amount)

    def compare(item1, item2):
        if type(item1) != type(item2):
            raise TypeError("Types of items compared not compatible")
        else:
            return item1 == item2

    def __add__(self,oth):
        if type(oth) != Money:
            raise TypeError("Cannot Add money to " + str(type(oth)))
        if oth.currency== self.currency:
            return  Money(self.amount + oth.amount, self.currency)
        else:
            raise TypeError("Trying to add different currencies")

    def __sub__(self,oth):
        if type(oth) != Money:
            raise TypeError("Cannot Subtract money to " + str(type(oth)))
        if oth.currency== self.currency:
            return Money(self.amount - oth.amount, self.currency)
        else:
            raise TypeError("Trying to subtract different currencies")

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other,float) or isinstance(other,Decimal):
            return Money(self.amount * other, self.currency)
        else:
            raise TypeError("Cannot Multiply money with" + str(type(other)))


class MoneyProxy(object):
    # sets the correct column names for this field.
    def __init__(self, field, name,type):
        self.field = field
        self.amount_field_name = name
        self.type= type
        self.currency_field_name = currency_field_name(name)

    def _get_values(self, obj):
        return (obj.__dict__.get(self.amount_field_name, None),
                obj.__dict__.get(self.currency_field_name, None))

    def _set_values(self, obj, amount, currency):
        obj.__dict__[self.amount_field_name] = amount
        obj.__dict__[self.currency_field_name] = currency

    def __get__(self, obj, *args):
        amount, currency = self._get_values(obj)
        if amount is None:
            return None

        return money_types[self.type](amount, Currency(currency))

    def __set__(self, obj, value):
        if value is None: # Money(0) is False
            self._set_values(obj, None, '')
        elif isinstance(value, money_types[self.type]):
            self._set_values(obj, value.amount, value.currency.iso)
        elif isinstance(value, Decimal):
            _, currency = self._get_values(obj) # use what is currently set
            self._set_values(obj, value, currency)
        else:

            if type(value) in money_types.values():
                raise TypeError("Trying to use " + str(type(value))+ ", expecting " + str(money_types[self.type]))
            # It could be an int, or some other python native type
            try:
                amount = Decimal(str(value))
                _, currency = self._get_values(obj) # use what is currently set
                self._set_values(obj, amount, currency)
            except TypeError:
                # Lastly, assume string type 'XXX 123' or something Money can
                # handle.
                try:
                    _, currency = self._get_values(obj) # use what is currently set
                    m = money_types[self.type].from_string(str(value))
                    self._set_values(obj, m.amount, m.currency)
                except TypeError:
                    msg = 'Cannot assign "%s"' % type(value)
                    raise TypeError(msg)


class CurrencyField(models.CharField):

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value


# Money describes a monetary value. It would be used to describe both cost and price values.
# Generally Money itself isn't used in business logic, instead, price and cost are used.
# This is intended as a 'smart'  version of a decimal, but in most cases you should look at Price, CostPrice or Cost,
# these are the droids you are looking for.
class MoneyField(models.DecimalField):
    description = ugettext_lazy('An amount and type of currency')

    def __init__(self, *args, **kwargs):

        kwargs['decimal_places'] = 5
        kwargs['max_digits'] = 28
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
        setattr(cls, name, MoneyProxy(self, name,self.type))

    # The boiler needs some plating
    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, money_types[self.type]):
            value = value.amount
            return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if isinstance(value,  money_types[self.type]):
            value = value.amount
            return super(MoneyField.get_prep_lookup(lookup_type, value))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.amount


# Cost describes the cost made for a certain thing.
# It could for instance describe the order cost related to a product on stock.
class Cost(Money):
    def compare(item1, item2):
        if type(item1) != type(item2):
            raise TypeError("Types of items compared not compatible")
        else:
            return item1 == item2

    def __add__(self,oth):
        if type(oth) != Cost:
            raise TypeError("Cannot Add money to " + str(type(oth)))
        if oth.currency== self.currency:
            return Cost(self.amount + oth.amount, self.currency)
        else:
            raise TypeError("Trying to add different currencies")

    def __sub__(self,oth):
        if type(oth) != Cost:
            raise TypeError("Cannot Subtract money to " + str(type(oth)))
        if oth.currency== self.currency:
            return Cost(self.amount - oth.amount, self.currency)
        else:
            raise TypeError("Trying to subtract different currencies")

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other,float) or isinstance(other,Decimal):
            return Cost(self.amount * other, self.currency)
        else:
            raise TypeError("Cannot Multiply money with" + str(type(other)))



    # What VAT level is it on


# A price describes a monetary value which is intended to be used on the sales side
class Price(Money):
    a=2


class PriceField(MoneyField):
    def __init__(self, *args, **kwargs):
        self.type ="price"
        super(MoneyField, self).__init__(args, kwargs)
    # What VAT level is it on?
    vat = models.ForeignKey(VAT)


class SalesPrice():
    pass


class SalesPriceProxy():
    pass


def cost_field_name(name):
    return "%cost" % name


def price_field_name(name):
    return "%price" % name


class SalesPriceField(PriceField):
    def contribute_to_class(self, cls, name):
        super(SalesPriceField).contribute_to_class(cls,price_field_name(name))
        cls.add_to_class(cost_field_name(name), CostField)
        # add the date field normally
        setattr(cls, self.name, SalesPriceProxy(self))


class TestMoneyType(models.Model):
    money = MoneyField(type="money")


class TestOtherMoneyType(models.Model):
    money = MoneyField(type="money")


class TestCostType(models.Model):
    money = MoneyField(type="cost")
#


# Define monetary types here
money_types = {}
money_types["cost"]=Cost
money_types["price"]= Price
money_types["money"] = Money
