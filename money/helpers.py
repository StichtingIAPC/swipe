from money.models import Currency, Money, Cost, Price
from tools.json_parsers import ParseError, DictParsers


class MoneyDictParsers:

    @staticmethod
    def money_parser(obj: dict):
        if obj is None:
            raise ParseError("Money does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Money as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        return Money(amount=amount, currency=currency)

    @staticmethod
    def cost_parser(obj: dict):
        if obj is None:
            raise ParseError("Cost does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Cost as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        return Cost(amount=amount, currency=currency)

    @staticmethod
    def price_parser(obj: dict, optional=False):
        if obj is None:
            if optional:
                return None
            else:
                raise ParseError("Price does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Price as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        vat = DictParsers.decimal_parser(obj.get("vat"))
        return Price(amount=amount, currency=currency, vat=vat)