import random
import re
import string

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.urls import reverse

from public_info import views

VALID_CHARS = string.ascii_letters + string.digits + '+-'


class Sharing(models.Model):
    random_str = models.CharField(
        max_length=16,
        editable=False,
        unique=True,
        validators=[
            RegexValidator(regex=re.compile(r'[' + VALID_CHARS + ']'))
        ],
        db_index=True)
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
        rnd = random.SystemRandom()
        random_str = ''.join([rnd.choice(VALID_CHARS) for i in range(20)])
        return reverse(
            'urlshare:shared',
            kwargs={
                'random_str': Sharing.objects.get_or_create(
                    sharing_type=ctype,
                    sharing_id=self.id,
                    defaults={
                        'random_str': random_str  # Will be the value if it did not exist already
                    }
                )[0].random_str
            }
        )

    def get_shared_view(self):
        views.get_public_view(type(self))

    class Meta:
        abstract = True


