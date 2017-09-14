from rest_framework import serializers


class ExternaliseDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'memo',
            'externalise_line_set'
        )


class ExternaliseLineSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'externalise_document',
            'article_type',
            'count',
            'cost'
        )
