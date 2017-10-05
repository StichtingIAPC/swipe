from django.db import models
from django.utils.translation import ugettext as _


class SoftDeletableQuerySet(models.QuerySet):
    def delete(self):
        for obj in self.all():
            obj.delete()

    def restore(self):
        for obj in self.all():
            obj.restore()


class SoftDeletableManager(models.Manager):
    """
    SoftDeletableManager modifies the default QuerySet to only return the active items.
    """

    def get_queryset(self):
        """
        :return: only active items
        """
        return SoftDeletableQuerySet(self.model).filter(is_deleted=False)

    def all_with_deleted(self):
        """
        :return: all items
        """
        return SoftDeletableQuerySet(self.model)

    def deleted(self):
        """
        :return: only deleted items
        """
        return SoftDeletableQuerySet(self.model).filter(is_deleted=True)


class SoftDeletable(models.Model):
    """
    SoftDeletable models the behaviour for a model to be soft deletable.
    """
    is_deleted = models.BooleanField(verbose_name=_('is deleted'), default=False)

    objects = SoftDeletableManager()

    def save(self, keep_deleted=False, **kwargs):
        if not keep_deleted:
            self.is_deleted = False
        super(SoftDeletable, self).save(**kwargs)

    def delete(self, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
        super(SoftDeletable, self).save(**kwargs)

    def restore(self, **kwargs):
        if self.is_deleted:
            self.is_deleted = False
        super(SoftDeletable, self).save(**kwargs)

    class Meta:
        abstract = True
