from rest_framework import serializers
from .models import Events


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'id',
            'date_created',
            'date_updated',
            'attendees',
            'event_date',
            'status',
            'notes',
            'client',
            'contract'
        ]
