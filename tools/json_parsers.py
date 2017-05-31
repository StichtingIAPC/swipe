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
    def list_parser(obj):
        if obj is None:
            raise ParseError("List is missing")
        if not isinstance(obj, list):
            raise ParseError("Object is not a list")
        return obj

    def int_parser(obj: int):
        if obj is None:
            raise ParseError("Integer is missing")
        if not isinstance(obj, int):
            raise ParseError("Object is not an integer")
        return obj


class ParseError(Exception):
    pass

