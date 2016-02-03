from django.db import models
from money.models import VAT
# Create your models here.


class ArticleType(models.Model):
    name = models.CharField()
    vat = models.ForeignKey(VAT)