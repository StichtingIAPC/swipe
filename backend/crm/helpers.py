from crm.models import Customer, User
from tools.json_parsers import ParseError


class CRMDictParsers:

    @staticmethod
    def user_parser(integer: int):
        if integer is None:
            raise ParseError("User does not exist")
        if not isinstance(integer, int):
            raise ParseError("User id is not integer")
        return User.objects.get(id=integer)

    @staticmethod
    def customer_parser(integer: int):
        if integer is None:
            raise ParseError("Customer does not exist")
        if not isinstance(integer, int):
            raise ParseError("Customer id is not integer")
        return Customer.objects.get(id=integer)
