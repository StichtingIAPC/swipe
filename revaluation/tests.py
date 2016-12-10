from django.test import TestCase
from tools.testing import TestData
from revaluation.models import RevaluationDocument

class RevaluationTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_fake_get_stock(self):
        RevaluationDocument.create_revaluation_document(self.user_1, [(self.articletype_1, self.cost_eur_1, None, None)])

