from django.template import Template
from django.utils.translation import ugettext_lazy as _

from tools.tables import Column


class MoneyColumn(Column):
    cell_template = Template("""<td>{{ value }}</td>""")
    name_templ = _("Cost ({currency_iso})")
    name = _("Cost")

    def __init__(self, *args, currency=None, **kwargs):
        """
        :param args:
        :param currency:
        :type currency: Currency
        :param kwargs:
        """
        if not kwargs['name'] and currency is not None:
            self.name = self.name_templ.format(currency_iso=currency.iso)
        super().__init__(*args, **kwargs)
