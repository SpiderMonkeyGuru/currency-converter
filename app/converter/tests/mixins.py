import datetime

from _decimal import Decimal
from rest_framework.test import APITestCase

from converter.models import ExchangeRate


class ExchangeRateTestMixin(APITestCase):
    def setUp(self) -> None:
        self.currency_code_EUR = 'EUR'
        self.currency_code_PLN = 'PLN'

        self.USD_to_EUR_rate_1 = Decimal('0.90123')
        self.USD_to_PLN_rate_1 = Decimal('4.01056')

        self.exchange_currency_1 = 'USD'

        self.exchange_rate_datetime_1 = datetime.datetime(2023, 7, 22, 1, 0, tzinfo=datetime.timezone.utc)
        self.exchange_rate_datetime_2 = datetime.datetime(2023, 7, 22, 13, 0, tzinfo=datetime.timezone.utc)
        self.exchange_rate_datetime_3 = datetime.datetime(2023, 7, 23, 1, 0, tzinfo=datetime.timezone.utc)
        self.exchange_rate_datetime_4 = datetime.datetime(2023, 7, 23, 13, 0, tzinfo=datetime.timezone.utc)

        self.PLN_USD_exchange_rate_4 = ExchangeRate.objects.create(
            currency_code=self.currency_code_PLN,
            rate=self.USD_to_PLN_rate_1,
            exchange_currency=self.exchange_currency_1,
            exchange_rate_datetime=self.exchange_rate_datetime_4
        )
        self.EUR_USD_exchange_rate_1 = ExchangeRate.objects.create(
            currency_code=self.currency_code_EUR,
            rate=self.USD_to_EUR_rate_1,
            exchange_currency=self.exchange_currency_1,
            exchange_rate_datetime=self.exchange_rate_datetime_1
        )
        self.EUR_USD_exchange_rate_2 = ExchangeRate.objects.create(
            currency_code=self.currency_code_EUR,
            rate=self.USD_to_EUR_rate_1,
            exchange_currency=self.exchange_currency_1,
            exchange_rate_datetime=self.exchange_rate_datetime_2
        )
        self.EUR_USD_exchange_rate_3 = ExchangeRate.objects.create(
            currency_code=self.currency_code_EUR,
            rate=self.USD_to_EUR_rate_1,
            exchange_currency=self.exchange_currency_1,
            exchange_rate_datetime=self.exchange_rate_datetime_3
        )
        self.EUR_USD_exchange_rate_4 = ExchangeRate.objects.create(
            currency_code=self.currency_code_EUR,
            rate=self.USD_to_EUR_rate_1,
            exchange_currency=self.exchange_currency_1,
            exchange_rate_datetime=self.exchange_rate_datetime_4
        )
