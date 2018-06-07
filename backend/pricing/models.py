from django.db import models
from django.core.exceptions import ValidationError
from article.models import SellableType, OtherCostType
from swipe.settings import USED_CURRENCY
from tools.util import raiseifnot
from money.models import Price, Money, Cost, SalesPrice
from decimal import Decimal
from crm.models import Customer
from stock.models import Stock
from supplier.models import ArticleTypeSupplier
from math import e


def validate_bigger_than_0(value):
    if value < 1:
        raise ValidationError("Value of pricingmodel should be bigger than 0")


# noinspection PyUnusedLocal
class PricingModel(models.Model):
    """
    This is a translater from row to actual processing function
    """
    exp_mult = models.DecimalField(max_digits=6, decimal_places=5)
    exponent = models.DecimalField(max_digits=6, decimal_places=5)
    constMargin = models.DecimalField(max_digits=6, decimal_places=5)
    min_relative_margin_error = models.DecimalField(max_digits=6, decimal_places=5)
    max_relative_margin_error = models.DecimalField(max_digits=6, decimal_places=5)
    custType = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT)

    @staticmethod
    def calc_price(cost: Cost,  vat_rate: Decimal, customer: Customer = None) -> Price:
        pm = PricingModel.objects.filter(custType=None).first()
        exp_mult = Decimal("0.15")
        exponent = Decimal("-0.18")
        constMargin =  Decimal("0.04")
        min_relative_margin_error = Decimal("0.2")
        max_relative_margin_error = Decimal("0.2")
        if pm != None:
            exp_mult = pm.exp_mult
            exponent = pm.exponent
            constMargin = pm.constMargin
            min_relative_margin_error = pm.min_relative_margin_error
            max_relative_margin_error = pm.max_relative_margin_error

        amount = (exp_mult * Decimal(Decimal(e) ** (exponent * cost.amount)) + constMargin+1)*cost.amount

        return SalesPrice(amount=Decimal(amount*vat_rate), vat=vat_rate, currency=cost.currency, cost=cost)

    @staticmethod
    def return_price(sellable_type: SellableType, customer: Customer = None,
                     stock: Stock = None) -> Price:
            if stock:
                cost = stock.book_value
            else:
                cost = Cost(amount=Decimal(1000000), currency=USED_CURRENCY)
            return PricingModel.calc_price(cost, sellable_type.get_vat_rate(), customer)


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
