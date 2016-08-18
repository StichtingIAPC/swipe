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
        typ = self._meta
        to_string=self.__str__()
        BlameLog.objects.create(type=typ,user_modified=self.user_modified,obj_pk=self.pk,to_string=to_string)


class ImmutableBlame(BasicBlame):
    class Meta:
        abstract = True

    def save(self, **kwargs):
        assert self.pk is None
        super(ImmutableBlame, self).save(kwargs)


class BlameTest(Blame):
    data = models.IntegerField()
    def __str__(self):
        return self.data.__str__()


class ImmutableBlameTest(ImmutableBlame):
    data = models.IntegerField()

class BlameLog(models.Model):
    type = models.CharField(max_length=64)
    date_modified = models.DateTimeField(auto_now_add=True)
    user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by")
    obj_pk = models.IntegerField()
    to_string = models.CharField(max_length=128)
    def __str__(self):
        return "{} {} @ {} > {} :{}".format(self.date_modified,self.user_modified.__str__().ljust(8)[:8],self.type.ljust(18)[:18], self.obj_pk.__str__().rjust(7," "), self.to_string)