from collections import defaultdict

from tools.tables.columns import *


class Table:
    """
    A generic class Table.

    usage: see views.TableView

    API:
    template: A Template instance, which receives this table's 'classes',
    'columns' and 'dataprovider' fields in its Context when rendering.

    render: add a special context. Normally only uses this class' data,
    but extra data can be injected if wanted.
    """

    template = Template("""
    <table class="{{ classes }}">
        <thead>
            <tr>{% for column in columns %}
                {{ column.header }}{% endfor %}
            </tr>
        </thead>
        <tbody>{% for row in dataprovider %}
            <tr>{% for column in columns %}
                {% include column with row=row only %}{% endfor %}
            </tr>{% empty %}
            <tr>
            <td class="empty" colspan="{{columns|length}}">Empty</td>
            </tr>{% endfor %}
        </tbody>
    </table>
    """)

    def __init__(self, columns=None, dataprovider=None, classes=None):
        """
        :param columns:
        :type columns: Tuple[Column, ...]
        :param dataprovider:
        :type dataprovider: Iterable
        :param classes:
        :type classes: Tuple[str, ...]
        """
        column_names = defaultdict(lambda: 0)
        count = 0
        for column in columns:
            if not column.key:
                column.key = lambda a: a[count+0]

            name = column.name
            if column_names[name]:
                column_names[name] += 1
                column.name += str(column_names[name])
                # Postfix any duplicate names with their occurance number, to make distinct names possible,
                # and ensure that keying the column names in json doesn't destoy data.
            else:
                column_names[name] += 1
        self.columns = columns

        self.dataprovider = dataprovider
        self.classes = classes

    def render(self, context=None):
        """
        :param context
        :type context: dict
        :return:
        :rtype: str
        """
        if context is None:
            context = {}
        context.update({
            'classes': self.classes_str(),
            'columns': self.columns,
            'dataprovider': self.dataprovider,
        })
        return self.template.render(context)

    def classes_str(self):
        """
        :rtype: str
        """
        return " ".join(self.classes)
