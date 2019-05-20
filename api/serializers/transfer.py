from rest_framework import serializers

from api.models import Transfer


class TransferSerializer(serializers.ModelSerializer):

    concept = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        model = Transfer
        fields = ('amount', 'receiver', 'concept',)


class FullTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = '__all__'
