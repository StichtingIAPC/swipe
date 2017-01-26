from django.db import models
from django.core.exceptions import ValidationError


def validate_bigger_than_0(value):
    if value < 1:
        raise ValidationError("Value of pricingmodel should be bigger than 0")


class PricingModel(models.Model):
    # A name indicates what the method does, not functional.
    name = models.CharField(max_length=40)
    # The priority of execution of the function. Lower number is higher priority. Number is bigger than 0 and unique.
    position = models.IntegerField(unique=True, null=False, validators=[validate_bigger_than_0])

    def __str__(self):
        return "Id: {}, Name: {}, Position: {}".format(self.id, self.name, self.position)
    
    def save(self):
        validate_bigger_than_0(self.position)
        super(PricingModel, self).save()

