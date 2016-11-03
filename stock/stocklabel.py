from django.core.validators import RegexValidator
from django.db import models

from stock.exceptions import StockLabelNotFoundError


class StockLabelQuerySet(models.QuerySet):

    @staticmethod
    def prepare_kwargs(kwargs):
        label = kwargs.pop("label", None)
        if label is not None:
            kwargs["labeltype"] = label.labeltype
            kwargs["labelkey"] = label.key
        if "labeltype" in kwargs.keys():
            if kwargs["labeltype"] == "":
                kwargs["labeltype"] = None
            if kwargs["labeltype"] is None:
                kwargs.pop("labelkey", None)
        return kwargs

    def get(self, *args, **kwargs):
        kwargs = self.prepare_kwargs(kwargs)
        return super().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        kwargs = self.prepare_kwargs(kwargs)
        return super().filter(*args, **kwargs)


class StockLabelManager(models.Manager):
    """
        StockLabelManager adds the option to get all Stock lines without a label. Shorthand for labeltype = None
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
    def register(cls, label_type):

        if label_type._labeltype == "":
            raise ValueError("Please use a more descriptive labeltype than '' (emptystring). "
                             "Use NoStockLabel when you want no stock label, "
                             "and search for None if you want to look for no label.")

        name = label_type._labeltype
        if cls.labeltypes is None:
            cls.labeltypes = {}
        if name in cls.labeltypes.keys():
            raise ValueError("StockLabel name '{}'  already in use for class {}".format(name, label_type))
        cls.labeltypes[name] = label_type
        return label_type

    # Returns correct label type
    @classmethod
    def return_label(cls, labeltype, key):

        if labeltype in cls.labeltypes.keys():
            lt = cls.labeltypes[labeltype]
        else:
            raise StockLabelNotFoundError("Stock label {} not found".format(labeltype))
        return lt(key)

    @property
    def labeltype(self):
        return self._labeltype

    def __init__(self, key=0):
        self._key = key
        if self._labeltype is None:
            raise ValueError("StockLabel's can't be created without a labeltype, "
                             "please create your own subclass of StockLabel")

        if self._labeltype == "":
            raise ValueError("Please use a more descriptive labeltype than '' (emptystring). "
                             "Use NoStockLabel when you want no stock label, "
                             "and search for None if you want to look for no label.")

    @property
    def key(self):
        return self._key

    def __eq__(self, other):
        if other is None and (self.labeltype is None or self.labeltype == ""):
            return True
        try:
            return other.key == self.key and other.labeltype == self.labeltype
        except Exception:
            return False

    def __str__(self):
        return "[{} : {}]".format(self.labeltype, self.key)

    def __hash__(self):
        return hash(self.labeltype)


class StockLabeledLine(models.Model):
    labeltype = models.CharField(max_length=255, null=True, blank=True, validators=[
        RegexValidator(regex='^.+$',
                       message='Labeltype should be longer than zero characters')
    ])
    labelkey = models.IntegerField(null=True, blank=True)
    objects = StockLabelManager()

    def __init__(self, *args, **kwargs):
        if kwargs.pop('labeltype', None) is not None:
            raise ValueError("labeltype should be kept at None, please use qualified argument 'label'")
        if kwargs.pop('labelkey', None) is not None:
            raise ValueError("labeltype should be kept at None, please use qualified argument 'label'")
        label = kwargs.pop('label', False)
        if label:
            kwargs["labeltype"] = label.labeltype
            kwargs["labelkey"] = label.key
        models.Model.__init__(self, *args, **kwargs)
        if hasattr(self, "id"):
            if self.labeltype:
                self.label = StockLabel.return_label(self.labeltype, self.labelkey)
            else:
                self.label = None

    class Meta:
        abstract = True


@StockLabel.register
class OrderLabel(StockLabel):
    _labeltype = "Order"
