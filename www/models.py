from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy

# Based on https://git.iapc.utwente.nl/swipe/swipe-design/issues/22


# VAT : Pay the government, alas, we have to do this.
class VAT (models.Model):
    # What's the Rate of this VAT (percentage)? This is the multiplication factor.
    rate = models.DecimalField(decimal_places=6, verbose_name=("VAT Rate"))
    # What's this VAT level called?
    name = models.CharField(max_lenth=255, verbose_name=("VAT Name"))
    # Is this VAT level in use?
    active = models.BooleanField()

    def to_rate_string(self):
        return ((self.rate-1)*100)+"%"


# Currency describes the currency of a monetary value. It's also used to describe the currency used in a till
class Currency(models.Model):
    # Currency name
    name = models.CharField(max_length=255, verbose_name=_("Currency"))

    # What symbol does this currency use?
    iso = models.CharField(max_length=32, verbose_name=("Iso Code"))

    # What symbol does this currency use?
    symbol = models.CharField(max_length=32, verbose_name=("Symbol"))

def currency_field_name(name):
    return "%s_currency" % name


class Money:
    def __init__(self,amount, currency):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return self.currency.iso+": "+self.amount

    def compare(item1, item2):
        if type(item1) != type(item2):
            raise TypeError("Types of items compared not compatible")
        else:
            return item1 == item2


class MoneyProxy(object):

# sets the correct column names for this field.
    def __init__(self, field, returnClass):
        self.field = field
        self.amount_field_name = field.name
        self.currency_field_name = currency_field_name(field.name)

    def _get_values(self, obj):
        return (obj.__dict__.get(self.field.amount_field_name, None),
                obj.__dict__.get(self.field.currency_field_name, None))

    def _set_values(self, obj, amount, currency):
        obj.__dict__[self.field.amount_field_name] = amount
        obj.__dict__[self.field.currency_field_name] = currency

    def __get__(self, obj, *args):
        amount, currency = self._get_values(obj)
        if amount is None:
            return None
        return Money(amount, currency)

    def __set__(self, obj, value):
        if value is None: # Money(0) is False
            self._set_values(obj, None, '')
        elif isinstance(value, Money):
            self._set_values(obj, value.amount, value.currency)
        elif isinstance(value, Decimal):
            _, currency = self._get_values(obj) # use what is currently set
            self._set_values(obj, value, currency)
        else:
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
                    m = Money.from_string(str(value))
                    self._set_values(obj, m.amount, m.currency)
                except TypeError:
                    msg = 'Cannot assign "%s"' % type(value)
                    raise TypeError(msg)


# Money describes a monetary value. It would be used to describe both cost and price values.
# Generally Money itself isn't used in business logic, instead, price and cost are used.
# This is intended as a 'smart'  version of a decimal, but in most cases you should look at Price, CostPrice or Cost,
# these are the droids you are looking for.
class MoneyField(models.DecimalField):
     description = ugettext_lazy('An amount and type of currency')

    # currency: Which currency is this money in?
    def contribute_to_class(self, cls, name):
        value = models.DecimalField(decimal_places=5)
        cls.add_to_class("currency", models.ForeignKey)
        value.creation_counter = self.creation_counter
        # add the date field normally
        super(MoneyField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MoneyProxy(self))

    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, Money):
            value = value.amount

        return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if isinstance(value, Money):
            value = value.amount
        return super(MoneyField, self).get_prep_lookup(lookup_type, value)


    def value_to_string(self, obj):
        """
        When serializing this field, we will output both value and currency.
        Here we only need to output the value. The contributed currency field
        will get called to output itself
        """
        value = self._get_val_from_obj(obj)
        return value.amount


# Cost describes the cost made for a certain thing.
# It could for instance describe the order cost related to a product on stock.
class CostField(MoneyField):
    def compare(item1, item2):
        if type(item1) != type(item2):
            raise TypeError("Types of items compared not compatible")
        else:
            return item1 == item2
    # What VAT level is it on

# TODO check for currency
class SumPrice:
    def __init__(self,prices):
        for price in prices:
            print price.money.value + " .." + price.vat


# A price describes a monetary value which is intended to be used on the sales side
class PriceField(MoneyField):
    # What VAT level is it on?
    vat = models.ForeignKey(VAT)
    def __add__(self,oth):
        if oth.vat == self.vat:
            c = Cost()
            c.money = Money()
            c.money.value = self.money.value + oth.money.value
        else:
            raise ValueError("Trying to add different VAT levels, this is not yet implemented")