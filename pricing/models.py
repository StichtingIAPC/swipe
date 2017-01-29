from django.db import models
from django.core.exceptions import ValidationError
from article.models import SellableType
from tools.util import raiseifnot
from money.models import Price, Money
from decimal import Decimal


def validate_bigger_than_0(value):
    if value < 1:
        raise ValidationError("Value of pricingmodel should be bigger than 0")


class PricingModel(models.Model):
    """
    This is a translater from row to actual processing function
    """
    # The primary key, also the key value reference to the function
    function_identifier = models.IntegerField(primary_key=True)
    # A name indicates what the method does, not functional.
    name = models.CharField(max_length=40)
    # The priority of execution of the function. Lower number is higher priority. Number is bigger than 0 and unique.
    position = models.IntegerField(unique=True, null=False, validators=[validate_bigger_than_0])

    def __str__(self):
        return "Id: {}, Name: {}, Position: {}".format(self.id, self.name, self.position)
    
    def save(self):
        validate_bigger_than_0(self.position)
        super(PricingModel, self).save()

    def return_pricing_function(self):
        """
        Retrieves a pricing function from its unique identifier
        :return:
        """
        function_dict = {1: Functions.fixed_price}

        return function_dict.get(self.function_identifier)

    @staticmethod
    def return_price(sellable_type: SellableType=None) -> Price:
        pricing_models = PricingModel.objects.all().order_by('function_identifier')
        if len(pricing_models) == 0:
            raise PricingError("No pricing models found!")
        else:
            price = None  # type: Price
            i = 0
            while price is None and i < len(pricing_models):
                pricing_function = pricing_models[i].return_pricing_function()
                if not pricing_function:
                    raise PricingError("Pricing function defined was not found")
                price = pricing_function(sellable_type=sellable_type)
                i += 1

            if not price:
                raise PricingError("Pricing models were applied and nothing appropriate was found. No price returned.")
            raiseifnot(price.uses_system_currency(), PricingError, "Returned price was not of system currency.")
            return price


class Functions:
    """
    A container class for all the pricing functions. All function should have the same arguments to accomodate
    seamless insertion of new pricing functions.

    """

    @staticmethod
    def fixed_price(sellable_type: SellableType=None):
        raiseifnot(isinstance(sellable_type, SellableType), TypeError, "sellableType should be sellableType")
        if hasattr(sellable_type, 'fixed_price'):
            fixed = sellable_type.fixed_price  # type: Money
            price = Price(amount=fixed.amount, currency=fixed.currency, vat=sellable_type.get_vat_rate())
            return price
        else:
            return None


class Rounding:
    """
    Simple rounding class. Rounds values according to listed values.
    """
    # Rounds to ROUNDING[i] if value <= ROUNDING_BRACKETS[i]
    ROUNDING_BRACKETS = [Decimal("1"), Decimal("15")]
    ROUNDING = [Decimal("0.05"), Decimal("0.2")]
    DEFAULT_ROUNDING = Decimal("0.5")

    @staticmethod
    def round_up(amount: Decimal) -> Decimal:
        """
        Rounds up to the next multiple of the ROUNDING element
        :param amount:
        :return:
        """
        i = 0
        while i < len(Rounding.ROUNDING_BRACKETS):
            if amount <= Rounding.ROUNDING_BRACKETS[i]:
                am = amount
                divved = am/Rounding.ROUNDING[i]
                divved_rounded = round(divved, 0)
                am_new = divved_rounded*Rounding.ROUNDING[i]
                if divved > divved_rounded:
                    am_new += Rounding.ROUNDING[i]
                # noinspection PyTypeChecker
                return am_new
            i += 1
        # We fall in no bounds, use default
        # Things break when rounding is done and div by zero occurs

        if Rounding.DEFAULT_ROUNDING > Decimal("0"):
            am = amount
            divved = am / Rounding.DEFAULT_ROUNDING
            divved_rounded = round(divved, 0)
            am_new = divved_rounded * Rounding.DEFAULT_ROUNDING
            if divved > divved_rounded:
                am_new += Rounding.DEFAULT_ROUNDING
            # noinspection PyTypeChecker
            return am_new
        # No rounding
        return amount


class PricingError(Exception):
    pass
