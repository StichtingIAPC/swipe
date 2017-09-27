from django.db import models
from django.core.exceptions import ValidationError
from article.models import SellableType, OtherCostType
from tools.util import raiseifnot
from money.models import Price, Money, Cost
from decimal import Decimal
from crm.models import Customer
from stock.models import Stock
from supplier.models import ArticleTypeSupplier


def validate_bigger_than_0(value):
    if value < 1:
        raise ValidationError("Value of pricingmodel should be bigger than 0")


# noinspection PyUnusedLocal
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

    # Add numerical properties of pricing models like the margin below.
    margin = models.DecimalField(null=True, blank=True, decimal_places=10, max_digits=16)

    def __str__(self):
        return "Id: {}, Name: {}, Position: {}".format(self.id, self.name, self.position)

    def save(self, *args, **kwargs):
        validate_bigger_than_0(self.position)
        super(PricingModel, self).save()

    def return_pricing_function(self):
        """
        Retrieves a pricing function from its unique identifier
        :return:
        """
        function_dict = {1: Functions.fixed_price,
                         2: Functions.fixed_margin}

        return function_dict.get(self.function_identifier)

    @staticmethod
    def return_price(sellable_type: SellableType = None, margin: Decimal = Decimal("0"), customer: Customer = None,
                     stock: Stock = None) -> Price:
        pricing_models = PricingModel.objects.all().order_by('position')
        if len(pricing_models) == 0:
            raise PricingError("No pricing models found!")
        else:
            price = None  # type: Price
            i = 0
            while price is None and i < len(pricing_models):
                pricing_function = pricing_models[i].return_pricing_function()
                if not pricing_function:
                    raise PricingError("Pricing function defined was not found")
                price = pricing_function(sellable_type, pricing_models[i], customer, stock)
                i += 1

            if not price:
                raise PricingError("Pricing models were applied and nothing appropriate was found. No price returned.")
            raiseifnot(price.uses_system_currency(), PricingError, "Returned price was not of system currency.")
            return price


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
class Functions:
    """
    A container class for all the pricing functions. All function should have the same arguments to accomodate
    seamless insertion of new pricing functions.
    """

    @staticmethod
    def fixed_price(sellable_type: SellableType = None, pricing_model: PricingModel = None, customer: Customer = None,
                    stock: Stock = None):
        if stock is not None and sellable_type is None:
            sellable_type = stock.article
        raiseifnot(isinstance(sellable_type, SellableType), TypeError, "sellableType should be sellableType")
        if hasattr(sellable_type, 'fixed_price'):
            fixed = sellable_type.fixed_price  # type: Money
            price = Price(amount=fixed.amount, currency=fixed.currency, vat=sellable_type.get_vat_rate())
            return price
        else:
            return None

    @staticmethod
    def fixed_margin(sellable_type: SellableType = None, pricing_model: PricingModel = None, customer: Customer = None,
                     stock: Stock = None):
        """
        Adds a desired margin and then rounds. Can either choose an articleType or a stock.
        :param sellable_type:
        :param pricing_model:
        :param customer:
        :param stock:
        :return:
        """
        margin = pricing_model.margin
        # If no margin is fed or margin is 0, we assume this does not process
        if not margin or margin == Decimal(0):
            return None
        # Stock contains all the necessary values for price calculation
        if stock:
            cst = stock.book_value  # type:Cost
            amt = cst.amount
            calcd = Rounding.round_up(amt * margin * stock.article.get_vat_rate())
            return Price(amount=calcd, currency=cst.currency, vat=stock.article.get_vat_rate())
        # If not stock, then we check the sellableType at the supplier side
        if sellable_type:
            # Othercosts do not have a margin and only posses a fixed price, use that.
            if isinstance(sellable_type, OtherCostType):
                fixed = sellable_type.fixed_price
                return Price(amount=fixed.amount, vat=sellable_type.get_vat_rate(), currency=fixed.currency)

            # We assume people are using ArticleTypes here
            atts = ArticleTypeSupplier.objects.filter(article_type=sellable_type, availability__in=['A', 'L'])
            if len(atts) == 0:
                return None
            lowest_price = atts[0].cost
            for att in atts:
                if att.cost < lowest_price:
                    lowest_price = att.cost

            calcd = Rounding.round_up(lowest_price.amount * margin * sellable_type.get_vat_rate())
            return Price(amount=calcd, currency=lowest_price.currency, vat=sellable_type.get_vat_rate())


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
                divved = am / Rounding.ROUNDING[i]
                divved_rounded = round(divved, 0)
                am_new = divved_rounded * Rounding.ROUNDING[i]
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
