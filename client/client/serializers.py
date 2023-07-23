from rest_framework import serializers

from client.models import CurrencyConvertionEventLog


class CurrencyConvertionEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConvertionEventLog
        fields = '__all__'
