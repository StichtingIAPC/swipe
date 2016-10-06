from django.shortcuts import render
from django.views import View

from stock.models import Stock
from tools.tables import Table, Column


class TableView(View):
    template_name = "tools/table_test.html"

    def get(self, request, *args, **kwargs):
        qs = Stock.objects.select_related('article').all()
        table = Table(
            columns=(
                Column(key=lambda row: row.article.id),
                Column(key=lambda row: row.article.name, name="ArticleName"),
                Column(key=lambda row: row.count, name="Amount of type"),
                Column(key=lambda row: row.book_value),
                Column(key=lambda row: row.labeltype, name="Labeltype"),
                Column(key=lambda row: row.labelkey, name="Labelkey"),
            ),
            dataprovider=qs,
            classes=('someclass', 'someotherclass'))
        return render(request, self.template_name, {'table': table})
