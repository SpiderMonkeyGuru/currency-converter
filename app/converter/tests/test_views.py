import datetime

from _decimal import Decimal
from django.test import RequestFactory
from rest_framework_api_key.models import APIKey

from converter.tests.mixins import ExchangeRateTestMixin


class CurrencyConverterViewSetTest(ExchangeRateTestMixin):
    def setUp(self):
        super().setUp()
        self.api_key, self.key = APIKey.objects.create_key(name="test-key")
        self.factory = RequestFactory()

    def test_convert(self):
        """ Test the convert action of the viewset """
        response = self.client.get(
            path='/currency-converter/convert/',
            data={
                'amount': '100',
                'from_currency': 'PLN',
                'to_currency': 'EUR',
                'date': '2023-07-23',
                'time': '12:00:00'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {self.key}'
            }
        )

        expected_result: dict = {
            'exchange_rate_datetime': datetime.datetime(2023, 7, 23, 13, 0, tzinfo=datetime.timezone.utc),
            'amount': Decimal('22.47143'),
            'currency': 'EUR'
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected_result)
