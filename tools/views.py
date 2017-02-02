from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views import View

from article.columns import ProductLabelsColumn
from stock.models import Stock
from tools.tables import Table, Column


class TableView(View):
    template_name = "tools/table_test.html"

    # noinspection PyUnusedLocal
    def get(self, request, *args, **kwargs):
        qs = Stock.objects\
            .select_related('article')\
            .prefetch_related('article__labels')\
            .all()

        table = Table(
            columns=(
                Column(key=lambda row: row.article.id),
                Column(key=lambda row: row.article.name, name=_("Article name")),
                ProductLabelsColumn(key=lambda row: row.article.assortmentlabel_set),
                Column(key=lambda row: row.count, name=_("Amount of type")),
                Column(key=lambda row: row.book_value),
                Column(key=lambda row: row.labeltype, name=_("Labeltype")),
                Column(key=lambda row: row.labelkey, name=_("Labelkey")),
            ),
            dataprovider=qs,
            classes=('someclass', 'someotherclass'))
        return render(request, self.template_name, {'table': table})
