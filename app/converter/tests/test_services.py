import datetime

from _decimal import Decimal

from converter.services import exchange_currencies
from converter.tests.mixins import ExchangeRateTestMixin


class ExchangeCurrenciesServiceTest(ExchangeRateTestMixin):
    def test_exchange_currencies(self):
        """ Test exchange_currencies function """
        result = exchange_currencies(
            amount=Decimal('100.0'),
            from_currency='PLN',
            to_currency='EUR',
            date=datetime.date(2023, 7, 23),
            time=datetime.time(12, 0, 0)
        )

        expected_result: dict = {
            'exchange_rate_datetime': datetime.datetime(2023, 7, 23, 13, 0, 0, tzinfo=datetime.timezone.utc),
            'amount': Decimal('22.47143'),
            'currency': 'EUR'
        }

        self.assertDictEqual(result, expected_result)
