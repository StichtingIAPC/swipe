#### Stock Labels
from django.core.validators import RegexValidator
from django.db import models

class StockLabelQuerySet(models.QuerySet):

    def prepare_kwargs(self,kwargs):
        label = kwargs.pop("label",None)
        if label is not None:
            kwargs["labeltype"]=label.labeltype
            kwargs["labelkey"] = label.key
        if "labeltype" in kwargs.keys():
            if kwargs["labeltype"]=="":
                kwargs["labeltype"] = None
            if  kwargs["labeltype"]==None:
                kwargs.pop("labelkey", None)
        return kwargs

    def get(self, *args, **kwargs):
        kwargs = self.prepare_kwargs(kwargs)
        return models.QuerySet.get(self,*args,**kwargs)

    def filter(self, *args, **kwargs):
        kwargs = self.prepare_kwargs(kwargs)
        return models.QuerySet.filter(self,*args,**kwargs)


class StockLabelManager(models.Manager):
    """
    SoftDeletableManager modifies the default QuerySet to only return the active items.
    """

    def get_queryset(self):
        """
        :return: only active items
        """
        return StockLabelQuerySet(self.model)

    def all_without_label(self):
         return StockLabelQuerySet(self.model).filter(labeltype=None)


class StockLabel:
    labeltypes = {}
    _labeltype = None

    # Adds labeltype to reverse lookup table (labeltypes)
    @classmethod
    def add_label_type(cls, type):
        if type._labeltype =="":
            raise ValueError("Please use a more descriptive labeltype than '' (emptystring). Use NoStockLabel when you want no stock label, and search for None if you want to look for no label.")

        name = type._labeltype
        if cls.labeltypes is None:
            cls.labeltypes = {}
        if name in cls.labeltypes.keys():
            raise ValueError("StockLabel name '{}'  already in used for class {}".format(name,type))
        cls.labeltypes[name] = type

    # Returns correct label type
    @classmethod
    def returnLabel(cls,labeltype, key):

        if labeltype in cls.labeltypes.keys():
            lt = cls.labeltypes[labeltype]
        else:
            lt= StockLabel
        return lt(key)

    @property
    def labeltype(self):
        return self._labeltype

    def __init__(self, key=0):
        self._key = key
        if self._labeltype == None:
            raise ValueError("StockLabel's can't be created without a labeltype, please create your own subclass of StockLabel")

        if self._labeltype =="":
            raise ValueError("Please use a more descriptive labeltype than '' (emptystring). Use NoStockLabel when you want no stock label, and search for None if you want to look for no label.")

    @property
    def key(self):
        return self._key

    def __bool__(self):
        return self.labeltype != ""

    def __eq__(self,other):
        if other is None and (self.labeltype is None or self.labeltype == ""):
            return True
        try:
            return other.key == self.key and other.labeltype == self.labeltype
        except Exception:
            return False

    def __str__(self):
        return "[{} : {}]".format(self.labeltype, self.key)


class StockLabeledLine(models.Model):
    labeltype = models.CharField(max_length=255,null=True, validators=[
    RegexValidator(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$',
                   message='Labeltype should be longer than zero characters')])
    labelkey = models.IntegerField(null=True)
    objects = StockLabelManager()

    def __init__(self, *args, **kwargs):
        if kwargs.pop('labeltype',None) is not None:
            raise ValueError("labeltype should be kept at None, please use qualified argument 'label'")
        if kwargs.pop('labelkey',None) is not None:
            raise ValueError("labeltype should be kept at None, please use qualified argument 'label'")
        label = kwargs.pop('label', False)
        if label:
            kwargs["labeltype"] = label.labeltype
            kwargs["labelkey"] = label.key
        models.Model.__init__(self,*args,**kwargs)

    @property
    def label(self):
        if self.labeltype:
            return StockLabel.returnLabel(self.labeltype, self.labelkey)
        return None

    class Meta:
        abstract = True