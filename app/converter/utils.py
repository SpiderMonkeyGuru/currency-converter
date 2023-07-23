import datetime
import logging

from _decimal import Decimal, ROUND_HALF_UP
from django.db.models import F, IntegerField, Func
from django.db.models.functions import Abs
from rest_framework.exceptions import ValidationError

from app.constants import ALLOWED_CURRENCIES
from converter.exceptions import CurrencyExchangeRateNotFound
from converter.models import ExchangeRate
from converter.serializers import ExchangeRateSerializer

logger = logging.getLogger(__name__)


class ExtractEpoch(Func):
    function = 'EXTRACT'
    template = "%(function)s('epoch' from %(expressions)s)"
    output_field = IntegerField()


def combine_date_and_time(
    exchange_rate_date: datetime.date,
    exchange_rate_time: datetime.time
) -> datetime.datetime:
    return datetime.datetime.combine(
        date=exchange_rate_date,
        time=exchange_rate_time
    )


def get_rate_closest_to_date(currency_code: str, date: datetime.datetime):
    annotated_qs = ExchangeRate.objects.filter(currency_code=currency_code).annotate(
        time_difference=Abs(
            ExtractEpoch(F('exchange_rate_datetime')) - ExtractEpoch(date.replace(tzinfo=datetime.timezone.utc))
        )
    )
    closest_object = annotated_qs.order_by('time_difference').first()
    if closest_object is None:
        raise CurrencyExchangeRateNotFound(detail=f'{currency_code}: Currency exchange rate not found.')
    return closest_object


def create_exchange_rates_from_currency_api_response(response_data: dict) -> None:
    for currency_code, exchange_rate_data in response_data.get('data').items():
        if currency_code not in ALLOWED_CURRENCIES:
            continue
        exchange_rate_data = {
            'currency_code': currency_code,
            'rate': Decimal(exchange_rate_data.get('value')).quantize(Decimal('0.00000'), rounding=ROUND_HALF_UP),
            'exchange_rate_datetime': response_data.get('meta').get('last_updated_at')
        }
        exchange_rate_serializer = ExchangeRateSerializer(data=exchange_rate_data)
        try:
            exchange_rate_serializer.is_valid(raise_exception=True)
            exchange_rate_serializer.save()
        except ValidationError as e:
            logger.error(e)
            continue
