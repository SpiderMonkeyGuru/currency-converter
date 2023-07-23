from _decimal import Decimal
from django.db import models

from app.models import UUIDPrimaryKeyTimestampedModel


class ExchangeRate(UUIDPrimaryKeyTimestampedModel):
    currency_code = models.CharField(max_length=3)
    rate = models.DecimalField(
        max_digits=20,
        decimal_places=5,
        default=Decimal(0)
    )
    exchange_currency = models.CharField(
        max_length=3,
        default='USD'
    )
    exchange_rate_datetime = models.DateTimeField()

    class Meta:
        ordering = ['-exchange_rate_datetime', 'currency_code']
