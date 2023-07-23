from _decimal import Decimal, ROUND_HALF_UP
from django.core.validators import MinValueValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.constants import ALLOWED_CURRENCIES
from converter.models import ExchangeRate


class UpperCaseCharField(serializers.CharField):
    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()


class ExchangeCurrenciesSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=5,
        validators=[MinValueValidator(Decimal(0))]
    )
    from_currency = UpperCaseCharField(max_length=3)
    to_currency = UpperCaseCharField(max_length=3)
    date = serializers.DateField()
    time = serializers.TimeField()

    def validate(self, attrs):
        super().validate(attrs)
        if not attrs.get('from_currency').upper() in ALLOWED_CURRENCIES:
            raise ValidationError({
                'from_currency': f'Unsupported currency: {attrs.get("from_currency").upper()}'
            })
        if not attrs.get('to_currency').upper() in ALLOWED_CURRENCIES:
            raise ValidationError({
                'to_currency': f'Unsupported currency: {attrs.get("to_currency").upper()}'
            })
        return attrs


class CurrencySerializer(serializers.Serializer):
    code = serializers.CharField()
    value = serializers.FloatField()


class LatestExchangeRatesMetaSerializer(serializers.Serializer):
    last_updated_at = serializers.DateTimeField()


class LatestExchangeRatesSerializer(serializers.Serializer):
    meta = LatestExchangeRatesMetaSerializer()
    data = serializers.DictField(child=CurrencySerializer())


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'modified_at')
