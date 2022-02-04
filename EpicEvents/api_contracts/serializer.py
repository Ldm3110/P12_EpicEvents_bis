from rest_framework import serializers

from api_contracts.models import Contracts


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = [
            'id',
            'date_created',
            'date_updated',
            'status',
            'amount',
            'payment_due',
            'client',
            'sales_contact'
        ]
        extra_kwargs = {
            'status': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'sales_contact': {'read_only': True}
        }
