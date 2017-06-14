from money.models import Denomination
from register.models import DenominationCount, Register
from tools.json_parsers import ParseError


class RegisterDictParsers:

    @staticmethod
    def denominationcount_parser(dictionary: dict):
        count = dictionary.get("count", None)
        if count is None:
            raise ParseError("Count is missing")
        if not type(count) == int:
            raise ParseError("Count is not an int")
        denomination = dictionary.get("denomination", None)
        if denomination is None:
            raise ParseError("Denomination is missing")
        if not type(denomination) == int:
            raise ParseError("Denomination is not an int")
        db_denom = Denomination.objects.get(id=denomination)
        return DenominationCount(denomination=db_denom, number=count)

    @staticmethod
    def register_parser(integer: int):
        if integer is None:
            raise ParseError("Register does not exist")
        if not type(integer) == int:
            raise ParseError("Register is not an int")
        return Register.objects.get(id=integer)