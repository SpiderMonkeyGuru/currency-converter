import datetime
from typing import Optional

from _decimal import Decimal, ROUND_HALF_UP

from converter.currency_api import CurrencyAPIClient
from converter.models import ExchangeRate
from converter.utils import combine_date_and_time, get_rate_closest_to_date, \
    create_exchange_rates_from_currency_api_response
from converter.validators import are_provided_currencies_valid


def exchange_currencies(
        amount: Decimal,
        from_currency: str,
        to_currency,
        date: datetime.date,
        time: datetime.time
) -> dict:
    are_provided_currencies_valid(from_currency, to_currency)

    _exchange_rate_datetime: datetime.datetime = combine_date_and_time(
        exchange_rate_date=date,
        exchange_rate_time=time
    )

    from_rate: ExchangeRate = get_rate_closest_to_date(
        currency_code=from_currency,
        date=_exchange_rate_datetime
    )
    to_rate: ExchangeRate = get_rate_closest_to_date(
        currency_code=to_currency,
        date=_exchange_rate_datetime
    )

    usd_amount: Decimal = amount / from_rate.rate
    to_amount: Decimal = usd_amount * to_rate.rate

    return {
        'exchange_rate_datetime': to_rate.exchange_rate_datetime,
        'amount': to_amount.quantize(Decimal('0.00000'), rounding=ROUND_HALF_UP),
        'currency': to_currency
    }


def retrieve_latest_exchange_rates(date: Optional[datetime.date] = None) -> None:
    response_data: dict = CurrencyAPIClient.retrieve_latest_exchange_rates(date)
    create_exchange_rates_from_currency_api_response(response_data)

