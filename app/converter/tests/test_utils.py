from datetime import datetime, date, time

from _decimal import Decimal

from converter.models import ExchangeRate
from converter.tests.mixins import ExchangeRateTestMixin
from converter.utils import combine_date_and_time, get_rate_closest_to_date


class UtilsTest(ExchangeRateTestMixin):
    def test_combine_date_and_time(self):
        """ Test combine_date_and_time function """
        d = date(2023, 7, 23)
        t = time(12, 0, 0)
        expected_datetime = datetime(2023, 7, 23, 12, 0, 0)
        self.assertEqual(combine_date_and_time(d, t), expected_datetime)

    def test_get_rate_closest_to_date(self):
        """ Test get_rate_closest_to_date function """
        self.assertEqual(
            get_rate_closest_to_date('EUR', datetime(2022, 7, 22, 15, 30, 0)),
            self.EUR_USD_exchange_rate_1
        )
        self.assertEqual(
            get_rate_closest_to_date('EUR', datetime(2023, 7, 22, 15, 30, 0)),
            self.EUR_USD_exchange_rate_2
        )
        self.assertEqual(
            get_rate_closest_to_date('EUR', datetime(2023, 7, 22, 22, 30, 0)),
            self.EUR_USD_exchange_rate_3
        )
        self.assertEqual(
            get_rate_closest_to_date('EUR', datetime(2023, 7, 24, 15, 30, 0)),
            self.EUR_USD_exchange_rate_4
        )