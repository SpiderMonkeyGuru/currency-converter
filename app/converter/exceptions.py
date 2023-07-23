from rest_framework.exceptions import APIException


class InvalidCurrency(APIException):
    status_code = 400
    default_code = 'invalid_currency'
    default_detail = 'Invalid currency'


class CurrencyExchangeRateNotFound(APIException):
    status_code = 404
    default_code = 'currency_exchange_rate_not_found'
    default_detail = 'Currency exchange rate not found'
