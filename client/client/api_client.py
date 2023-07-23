import datetime
from _decimal import Decimal

import requests
from django.conf import settings
from requests import Response


class ApiClient:
    def __init__(self):
        self.url = 'http://backend:8000/currency-converter/convert/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {settings.CURRENCY_CONVERTER_API_KEY}'
        }

    def convert_currency(
            self,
            amount: Decimal,
            source_currency: str,
            destination_currency: str,
            date: datetime.date,
            time: datetime.time
    ) -> Response:
        response: Response = requests.get(
            url=self.url,
            params={
                'amount': amount,
                'from_currency': source_currency,
                'to_currency': destination_currency,
                'date': date,
                'time': time,

            },
            headers=self.headers
        )
        return response
