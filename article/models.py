from django.db import models
# from money.models import VAT
# Create your models here.


class ArticleType(models.Model):
    intf = models.IntegerField(default=2)
