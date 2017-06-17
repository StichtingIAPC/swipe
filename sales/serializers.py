from collections import OrderedDict

from rest_framework import serializers

from sales.models import Payment, TransactionLine, SalesTransactionLine, Transaction, \
    OtherCostTransactionLine, OtherTransactionLine, RefundTransactionLine
from money.serializers import MoneySerializerField, PriceSerializer, CostSerializerField


class PaymentSerializer(serializers.ModelSerializer):

    amount = MoneySerializerField()

    class Meta:
        model = Payment
        fields = (
            'id',
            'payment_type',
            'amount',
            'transaction'
        )


class TransactionSerializer(serializers.Serializer):

    def to_representation(self, instance: Transaction):
        data = OrderedDict()
        data["id"] = instance.id
        data["salesperiod"] = instance.salesperiod_id
        data["customer"] = instance.customer_id
        lines = instance.transactionline_set.select_related('othercosttransactionline',
                                                            'salestransactionline', 'othertransactionline',
                                                            'refundtransactionline')
        serialized_lines = []
        for line in lines:
            if hasattr(line, 'othercosttransactionline') and line.othercosttransactionline is not None:
                serialized_lines.append(OtherCostTransactionLineSerializer().to_representation(line.othercosttransactionline))
            if hasattr(line, 'salestransactionline') and line.salestransactionline is not None:
                serialized_lines.append(SalesTransactionLineSerializer().to_representation(line.salestransactionline))
            if hasattr(line, 'othertransactionline') and line.othertransactionline is not None:
                serialized_lines.append(OtherTransactionLineSerializer().to_representation(line.othertransactionline))
            if hasattr(line, 'refundtransactionline') and line.refundtransactionline is not None:
                serialized_lines.append(None)

        data["transactions"] = serialized_lines
        payments = Payment.objects.filter(id=instance.id)
        serialized_payments = []
        for payment in payments:
            serialized_payments.append(PaymentSerializer().to_representation(payment))
        data["payments"] = serialized_payments
        return data


class TransactionLineSerializer(serializers.Serializer):

    def to_representation(self, instance: TransactionLine):
        data = OrderedDict()
        data['id'] = instance.id
        data['transaction'] = instance.transaction_id
        data['num'] = instance.num
        data['price'] = PriceSerializer().to_representation(instance.price)
        data['count'] = instance.count
        data['isRefunded'] = instance.isRefunded
        data['text'] = instance.text
        data['order'] = instance.order
        data['accounting_group'] = instance.accounting_group_id
        data['original_price'] = PriceSerializer().to_representation(instance.original_price)
        data['class'] = "TransactionLine"
        return data


class SalesTransactionLineSerializer(TransactionLineSerializer):

    def to_representation(self, instance: SalesTransactionLine):
        data = super(SalesTransactionLineSerializer, self).to_representation(instance)
        data['cost'] = CostSerializerField().to_representation(instance.cost)
        data['article'] = instance.article_id
        data['class'] = "SalesTransactionLine"
        return data


class OtherCostTransactionLineSerializer(TransactionLineSerializer):

    def to_representation(self, instance: OtherCostTransactionLine):
        data = super(OtherCostTransactionLineSerializer, self).to_representation(instance)
        data['other_cost_type'] = instance.other_cost_type_id
        data['class'] = "OtherCostTransactionLine"
        return data


class OtherTransactionLineSerializer(TransactionLineSerializer):

    def to_representation(self, instance: OtherTransactionLine):
        data = super(OtherTransactionLineSerializer, self).to_representation(instance)
        data['class'] = "OtherTransactionLine"
        return data


class RefundTransactionLineSerializer(TransactionLineSerializer):

    def to_representation(self, instance: RefundTransactionLine):
        data = super(RefundTransactionLineSerializer, self).to_representation(instance)
        data['sold_transaction_line'] = instance.sold_transaction_line_id
        data['test_rma'] = instance.test_rma_id
        data['creates_rma'] = instance.creates_rma
        data['class'] = "RefundTransactionLine"
        return data


