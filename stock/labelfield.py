#### Stock Labels
from django.db import models
from django.utils.translation import ugettext_lazy


class LabelQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        label = kwargs.pop("label",None)
        if label:
            kwargs["labeltype"]=label.labeltype
            kwargs["labelkey"] = label.key
        return models.QuerySet.get(self,*args,**kwargs)

    def filter(self, *args, **kwargs):
        label = kwargs.pop("label",None)
        if label:
            kwargs["labeltype"]=label.labeltype
            kwargs["labelkey"] = label.key

        return models.QuerySet.filter(self,*args,**kwargs)


class LabelManager(models.Manager):
    """
    SoftDeletableManager modifies the default QuerySet to only return the active items.
    """

    def get_queryset(self):
        """
        :return: only active items
        """
        return LabelQuerySet(self.model)

    def all_without_label(self):
         return LabelQuerySet(self.model).filter(labeltype=None)


class Label:
    labeltypes = {}
    _labeltype = None

    # Adds labeltype to reverse lookup table (labeltypes)
    @classmethod
    def add_label_type(cls, name, type):
        if cls.labeltypes is None:
            cls.labeltypes = {}
        cls.labeltypes[name] = type

    # Registers label for use
    def register(self):
        Label.add_label_type(self.labeltype,type(self))
        print(type(self))

    # Returns correct label type
    @classmethod
    def returnLabel(cls,labeltype, key):
        if labeltype in cls.labeltypes.keys():
            lt = cls.labeltypes[labeltype]
        else:
            lt= Label
        return lt(key)

    @property
    def labeltype(self):
        return self._labeltype

    def __init__(self,labeltype="", key=0):
        self._labeltype = labeltype
        self._key = key

    @property
    def key(self):
        return self._key

    def __eq__(self,other):
        try:
            return other.key == self.key and other.labeltype == self.labeltype
        except Exception:
            return False

    def __str__(self):
        return "[{} : {}]".format(self.labeltype, self.key)


class NoLabel(Label):
    def __init__(self, key=0):
        Label.__init__(self,"",key)
        Label.register(self)

    def __str__(self):
        return "____"


class ZLabel(Label):
    def __init__(self, key=0):
        Label.__init__(self,"Z",key)
        Label.register(self)


class TestLabel(Label):
    def __init__(self, key=0):
        Label.__init__(self,"test",key)
        Label.register(self)


class StockLabeledLine(models.Model):
    labeltype = models.CharField(max_length=255,null=True)
    labelkey = models.IntegerField(null=True)
    objects = LabelManager()

    def __init__(self, *args, **kwargs):
        label = kwargs.pop('label', False)
        if label:
            kwargs["labeltype"] = label.labeltype
            kwargs["labelkey"] = label.key
        models.Model.__init__(self,*args,**kwargs)

    @property
    def label(self):
        if self.labeltype:
            return Label.returnLabel(self.labeltype, self.labelkey)
        return None

    class Meta:
        abstract = True

