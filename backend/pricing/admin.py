from django.contrib import admin

# Register your models here.
from pricing.models import PricingModel

admin.site.register(PricingModel)
