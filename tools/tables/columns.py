from django.template import Template


class Column:
    header_template = Template("""<td>{{ name }}</td>""")
    cell_template = Template("""<td>{{ value }}</td>""")

    def __init__(self, *args, key=lambda row: 0, name=None):
        """
        :param args:
        :type args: Tuple[Any, ...]
        :param key:
        :type key: Callable[[Any], Any]
        :return:
        """
        self.key = key
        if name is None:
            if self.name is None:
                self.name = str(type(self))
        else:
            self.name = name

    def render_header(self):
        """
        :return:
        :rtype: str
        """
        return self.header_template.render({"name": self.name})

    def render(self, context):
        """
        :param row:
        :type row: Any
        :return: the value of this cell
        :rtype: Any
        """
        return self.cell_template.render({"value": self.key(context['row'])})

    def set_name(self, name):
        """
        :param name:
        :type name: str
        """
        self.name = name

    def jsonify_data(self, row):
        """
        :param row:
        :type row: Any
        :return:
        :rtype: Any
        """
        return {'result': self.key(row)}
