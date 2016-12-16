from django.contrib.auth.models import User
from django.db import models, transaction

from tools.util import raiseif


class BasicBlame(models.Model):
    """
        Basic blame type
    """
    class Meta:
        abstract = True
    date_created = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by")


class Blame(BasicBlame):
    """
        Use this class to track who created and modified a model.

        Set the user_modified property of a subclass of this with the user that modified it.
        Do NOT set the user_created property; that property is set by the save function.

    """
    class Meta:
        abstract = True
    date_modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by")

    def save(self, **kwargs):
        if not self.user_created_id:
            self.user_created = self.user_modified
        super(Blame, self).save(kwargs)
        typ = self._meta
        to_string = self.__str__()
        BlameLog.objects.create(
            type=typ,
            user_modified=self.user_modified,
            obj_pk=self.pk,
            to_string=to_string)


class ImmutableBlame(BasicBlame):
    """
        Use this class to track who created a model, and prevent further saves to it.

        Set the user_created property of a subclass of this with the user that created it.
        This one has no user_modified property, for obvious reasons.
    """
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        kwargs["user_created"] = kwargs.get("user_created", kwargs.get("user_modified", None))
        kwargs.pop("user_modified", None)
        super(ImmutableBlame, self).__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, **kwargs):
        if not hasattr(self, "user_created") and hasattr(self, "user_modified"):
            self.user_created = self.user_modified
            delattr(self, "user_modified")

        raiseif(self.pk is not None,
                ImmutableBlameEditException,
                "you are trying to edit an immutable blame. That is not "
                "something you can do, so don't do that")

        super(ImmutableBlame, self).save(kwargs)
        typ = self._meta
        to_string = self.__str__()
        BlameLog.objects.create(
            type=typ,
            user_modified=self.user_created,
            obj_pk=self.pk,
            to_string=to_string)


class BlameLog(models.Model):
    """
        Keep track of who edited Blame'd models and when.
    """
    type = models.CharField(max_length=64)
    date_modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by")
    obj_pk = models.IntegerField()
    to_string = models.CharField(max_length=128)

    def __str__(self):
        return "{} {} @ {} > {} :{}".format(self.date_modified, self.user_modified.__str__().ljust(8)[:8],
                                            self.type.ljust(18)[:18], self.obj_pk.__str__().rjust(7, " "),
                                            self.to_string)


class BlameTest(Blame):
    """
        Mock model for unit tests
    """
    data = models.IntegerField()

    def __str__(self):
        return self.data.__str__()


class ImmutableBlameTest(ImmutableBlame):
    """
        Mock model for unit tests
    """
    data = models.IntegerField()


class ImmutableBlameEditException(Exception):
    """
    An exception thrown when you are trying to edit an immutable blame.
    """
    pass
