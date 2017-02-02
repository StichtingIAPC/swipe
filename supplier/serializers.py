from rest_framework import serializers

from supplier.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'search_url',
            'notes',
            'is_used',
            'is_backup',
        )
