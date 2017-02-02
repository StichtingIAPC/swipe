from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _

from tools.tables import Column


class ProductLabelsColumn(Column):
    """
        Product label column. Point it the labelset of a product, and it will render all labels that are known.
    """
    cell_template = Template("""{% load i18n %}
                                <td>{% for label in labels %}
                                    <span class="label">
                                        {{ label }}
                                    </span> {% empty %}
                                    {% trans 'No labels' %}
                                {% endfor %}</td>""")
    name = _('Labels')

    def get_context(self, row):
        return Context({'labels': row})
