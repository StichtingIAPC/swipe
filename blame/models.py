from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BasicBlame(models.Model):
    class Meta:
        abstract = True
    date_created = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by")


class Blame(BasicBlame):
    class Meta:
        abstract = True
    date_modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by")

    def save(self, **kwargs):
        if not self.user_created_id:
            self.user_created = self.user_modified
        super(Blame, self).save(kwargs)


class ImmutableBlame(BasicBlame):
    class Meta:
        abstract = True

    def save(self, **kwargs):
        assert self.pk is None
        super(ImmutableBlame, self).save(kwargs)


class BlameTest(Blame):
    data = models.IntegerField()


class ImmutableBlameTest(ImmutableBlame):
    data = models.IntegerField()
