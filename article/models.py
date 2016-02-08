from django.db import models
# from money.models import VAT
# Create your models here.


class ArticleType(models.Model):
    intf = models.IntegerField(default=2)
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name
