import datetime

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

    def validate(self, data):
        """
        Check that the event date is after the current date.
        """
        if data['event_date'] < datetime.datetime.now().date():
            raise serializers.ValidationError({"event_date": "This date must be after the current date"})
        return data
