#### Stock Labels
from django.db import models
from django.utils.translation import ugettext_lazy


class Label:
    def __init__(self,labeltype, key):
        self._labeltype = labeltype
        self._key = key

    @property
    def key(self):
        return self._key

    @property
    def labeltype(self):
        return self._labeltype

    def __eq__(self,other):
        if type(other) != Label:
            return False
        return other.key == self.key and other.labeltype == self.labeltype

    def __str__(self):
        return "[{} : {}]".format(self.labeltype, self.key)


class StockLabeledLine(models.Model):
    labeltype = models.CharField(max_length=255,null=True)
    labelkey = models.IntegerField(null=True)

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label', False)
        if label:
            kwargs["labeltype"] = label.labeltype
            kwargs["labelkey"] = label.key
        models.Model.__init__(self,*args,**kwargs)

    @property
    def label(self):
        if self.labeltype:
            return Label(self.labeltype, self.labelkey)
        return None

    class Meta:
        abstract = True
