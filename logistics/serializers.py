from rest_framework import serializers

from logistics.models import SupplierOrder


class SupplierOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierOrder
        fields = (
            'supplier'
        )
