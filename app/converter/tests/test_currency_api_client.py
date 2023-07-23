import datetime
from unittest.mock import patch

from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from app.currency_api import client as currency_api_client
from converter.currency_api import CurrencyAPIClient
from converter.serializers import LatestExchangeRatesSerializer


class TestCurrencyAPIClient(APITestCase):
    def setUp(self):
        self.mock_api_response = {
            "meta": {
                "last_updated_at": "2023-06-23T10:15:59Z"
            },
            "data": {
                "AED": {
                    "code": "AED",
                    "value": 3.67306
                },
                "AFN": {
                    "code": "AFN",
                    "value": 91.80254
                },
                "ALL": {
                    "code": "ALL",
                    "value": 108.22904
                },
                "AMD": {
                    "code": "AMD",
                    "value": 480.41659
                }
            }
        }

        self.client = CurrencyAPIClient()

    @patch.object(currency_api_client, 'latest')
    def test_retrieve_latest_exchange_rates_without_date(self, mock_latest):
        mock_latest.return_value = self.mock_api_response
        result = self.client.retrieve_latest_exchange_rates()

        mock_latest.assert_called_once_with()
        self.assertIsInstance(result, dict)
        self.assertDictEqual(result, LatestExchangeRatesSerializer(self.mock_api_response).data)

    @patch.object(currency_api_client, 'historical')
    def test_retrieve_latest_exchange_rates_with_date(self, mock_historical):
        mock_historical.return_value = self.mock_api_response
        date = datetime.date(2023, 6, 23)

        result = self.client.retrieve_latest_exchange_rates(date)

        mock_historical.assert_called_once_with(date=date)
        self.assertIsInstance(result, dict)
        self.assertDictEqual(result, LatestExchangeRatesSerializer(self.mock_api_response).data)

    @patch.object(currency_api_client, 'latest')
    def test_retrieve_latest_exchange_rates_invalid_response(self, mock_latest):
        mock_latest.return_value = {'invalid': 'response'}

        with self.assertRaises(ValidationError):
            self.client.retrieve_latest_exchange_rates()