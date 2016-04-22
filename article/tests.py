from django.test import TestCase
from article.models import *


class ArticleBasicTests(TestCase):

    def setUp(self):
        pass

    def test_save(self):
        generic_wishable_type = WishableType()
        generic_wishable_type.name = "foo"
        blocked = False
        try:
            generic_wishable_type.save()
        except AbstractClassInitializationError:
            blocked = True
        assert blocked


