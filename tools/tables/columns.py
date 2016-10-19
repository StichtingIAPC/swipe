from django.template import Template, Context


class Column:
    """
    Generic column class.
    Uses basic templates for its column header and cell values.
    If you want different templates, or other behaviour, feel free to subclass.
    Example usages in money.columns and in article.columns

    API:
    header_template: Instance of django.template.Template. Context contains 'name'
    with the column's name.

    cell_template: Instance of django.template.Template. Context contains 'value'
    with that cell's value. The value is currently extracted from the data row in
    the Column.render function, using the Column.key method.

    name: name does default to the 'name' property specified by a subclass, or (if
    not available) the stringified name of the class.

    get_context: Get the context for the cell renderer. Default returns only
    {value: value}, but may be extended.

    """
    header_template = Template("""<td>{{ name }}</td>""")
    cell_template = Template("""<td>{{ value }}</td>""")

    def __init__(self, *args, key=lambda row: 0, name=None):
        """
        :param args:
        :type args: Tuple[Any, ...]
        :param key: the way to extract this column's data from each row
        :type key: Callable[[Any], Any]
        :param name: Header name of this column. Should be unique. May be used in transmitting data.
        :type name: str
        """
        self.key = key
        if name is None:
            if not hasattr(self, 'name'):
                self.name = type(self).__name__
        else:
            self.name = name

    def header(self):
        """
        :return:
        :rtype: str
        """
        ctx = Context({"name": self.name})
        return self.header_template.render(ctx)

    def render(self, context):
        """
        :param context: the context given in the include tag. Only
        :type context: Context
        :return: the rendered template of this column cell
        :rtype: str
        """
        return self.cell_template.render(self.get_context(context['row']))

    def get_context(self, row):
        """
        :param row:
        :type row: Any
        :return:
        """
        return Context({"value": self.key(row)})

    def jsonify_data(self, row):
        """
        :param row:
        :type row: Any
        :return:
        :rtype: Any
        """
        return {'result': self.key(row)}
