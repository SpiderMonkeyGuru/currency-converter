from _decimal import Decimal

from app.models import UUIDPrimaryKeyTimestampedModel
from django.db import models


class CurrencyConvertionEventLog(UUIDPrimaryKeyTimestampedModel):
    api_request_amount = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        default=Decimal(0),
    )
    api_request_from_currency = models.CharField(max_length=3)
    api_response_converted_amount = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        null=True,
        default=None
    )
    api_request_to_currency = models.CharField(max_length=3)
    api_request_exchange_rate_datetime = models.DateTimeField()
    api_response_exchange_rate_datetime = models.DateTimeField(null=True)
    api_response_status_code = models.PositiveSmallIntegerField()
    api_response_body = models.JSONField()

