import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.views import View


class Sharing(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    public = models.BooleanField(default=True)

    sharing_type = models.ForeignKey(ContentType)
    sharing_id = models.PositiveIntegerField()
    sharing_object = GenericForeignKey(
        ct_field='sharing_type',
        fk_field='sharing_id',
    )


class Shared(models.Model):
    sharing_object = GenericRelation(
        Sharing,
        content_type_field='sharing_type',
        object_id_field='sharing_id'
    )

    def get_shared_url(self):
        ctype = ContentType.objects.get_for_model(type(self))
        return reverse('urlshare:shared', kwargs={
                'uuid_str': Sharing.objects.get_or_create(
                    sharing_type=ctype,
                    sharing_id=self.id,
                )[0].uuid.hex
            }
        )

    def get_shared_view(self):
        return get_public_view(type(self))

    class Meta:
        abstract = True


PUBLIC_VIEWS = {}


def get_public_view(cls_type):
    if PUBLIC_VIEWS[cls_type]:
        return PUBLIC_VIEWS[cls_type]
    raise SharedViewNotFoundException


def public_view(model=None):
    """
    Decorator to say 'this view has the view logic for this model type'
    :param model: the model it makes visible
    :return:
    """
    def decorate(view):
        if issubclass(view, View):
            view = view.as_view()
        PUBLIC_VIEWS[model] = view
        return view
    return decorate


class SharedViewNotFoundException(Exception):
    pass
