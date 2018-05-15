from article.helpers import ArticleDictParsers
from crm.helpers import CRMDictParsers
from money.helpers import MoneyDictParsers
from sales.models import Payment, SalesTransactionLine, OtherCostTransactionLine, OtherTransactionLine, \
    RefundTransactionLine, PriceOverride
from tools.json_parsers import ParseError, DictParsers


class SalesDictParsers:

    @staticmethod
    def payment_parser(obj: dict):
        if obj is None:
            raise ParseError("Payment does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Payment is not a dict")
        payment_type = DictParsers.int_parser(obj.get("payment_type"))
        amount = MoneyDictParsers.money_parser(obj.get("amount"))
        return Payment(payment_type_id=payment_type, amount=amount)

    @staticmethod
    def price_override_parser(obj: dict):
        if obj is None:
            return None
        if not isinstance(obj, dict):
            raise ParseError("PriceOverride is not a dict")
        user = CRMDictParsers.user_parser(obj.get("user"))
        reason = DictParsers.string_parser(obj.get("reason"))
        original_price = MoneyDictParsers.price_parser(obj.get("original_price"))
        return PriceOverride(user=user, reason=reason, original_price=original_price)


    @staticmethod
    def transactionline_parser(obj: dict):
        count = DictParsers.int_parser(obj.get("count"))
        price = MoneyDictParsers.price_parser(obj.get("price"))
        order = DictParsers.int_parser(obj.get("order"), optional=True)
        original_price = SalesDictParsers.price_override_parser(obj.get("original_price"))
        clazz = DictParsers.string_parser(obj.get("class"))
        if clazz == "SalesTransactionLine":
            cost = MoneyDictParsers.cost_parser(obj.get("cost"))
            article = ArticleDictParsers.article_parser(obj.get("article"))
            return SalesTransactionLine(count=count, price=price, order=order,
                                        cost=cost, article=article, original_price=original_price)
        elif clazz == "OtherCostTransactionLine":
            other_cost_type = DictParsers.int_parser(obj.get("other_cost_type"))
            return OtherCostTransactionLine(count=count, price=price, order=order,
                                            other_cost_type_id=other_cost_type, original_price=original_price)
        elif clazz == "OtherTransactionLine":
            text = DictParsers.string_parser(obj.get("text"))
            accounting_group = DictParsers.int_parser(obj.get("accounting_group"))
            return OtherTransactionLine(count=count, price=price, order=order,
                                        text=text, accounting_group_id=accounting_group, original_price=original_price)
        elif clazz == "RefundTransactionLine":
            sold_transaction_line = DictParsers.int_parser(obj.get("sold_transaction_line"))
            test_rma = DictParsers.int_parser(obj.get("test_rma"), optional=True)
            creates_rma = DictParsers.boolean_parser(obj.get("creates_rma"), optional=True)
            if not creates_rma:
                creates_rma = False
            return RefundTransactionLine(count=count, price=price, order=order,
                                         sold_transaction_line_id=sold_transaction_line, test_rma=test_rma,
                                         creates_rma=creates_rma, original_price=original_price)
        else:
            raise ParseError("Class is not valid")