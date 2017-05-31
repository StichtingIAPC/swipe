from decimal import Decimal


class DictParsers():
    @staticmethod
    def decimal_parser(string: str):
        if string is None:
            raise ParseError("String does not exist")
        try:
            float(string)
        except ValueError:
            raise ParseError("String is not a valid decimal")
        return Decimal(string)

    @staticmethod
    def string_parser(string: str):
        if string is None:
            raise ParseError("String does not exist")
        return string

    @staticmethod
    def list_parser(obj: str):
        if obj is None:
            raise ParseError("List is missing")
        if not isinstance(obj, list):
            raise ParseError("Object is not a list")
        return obj


class ParseError(Exception):
    pass

