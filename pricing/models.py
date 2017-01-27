from django.db import models
from django.core.exceptions import ValidationError
from article.models import SellableType
from tools.util import raiseifnot


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

        return function_dict.get(self.id)

    @staticmethod
    def return_price(sellable_type: SellableType=None):
        pricing_models = PricingModel.objects.all().order_by('function_identifier')
        if len(pricing_models) == 0:
            raise PricingError("No pricing models found!")
        else:
            price = None
            i=0
            while price is None and i < len(pricing_models):
                pricing_function = pricing_models[i].return_pricing_function()
                price = pricing_function(sellable_type=sellable_type)
                i+=1

            if not price:
                raise PricingError("Pricing models were applied and nothing appropriate was found. No price returned.")

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
            return sellable_type.fixed_price
        else:
            return None


class PricingError(Exception):
    pass