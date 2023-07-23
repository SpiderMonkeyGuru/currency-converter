import datetime
from _decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand, CommandError
from requests import ConnectionError, Timeout, TooManyRedirects
from rest_framework.exceptions import ValidationError

from client.api_client import ApiClient
from client.serializers import CurrencyConvertionEventLogSerializer


class Command(BaseCommand):
    help = 'This commands converts the given amount of source currency, to the destination currency'
    name = 'convert_currency'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=str, help='Amount to convert')
        parser.add_argument('--from-currency', type=str, help='Source currency')
        parser.add_argument('--to-currency', type=str, help='Destination currency')
        parser.add_argument('--date', type=str, help='Date of the exchange rate')
        parser.add_argument('--time', type=str, help='Time of the exchange rate')

    def handle(self, *args, **options):
        amount: Decimal = self._convert_string_to_decimal_amount(
            self._get_required_argument_value('amount', options)
        )
        from_currency: str = self._get_required_argument_value('from_currency', options)
        to_currency: str = self._get_required_argument_value('to_currency', options)
        date: datetime.date = self._convert_string_to_date(
            self._get_required_argument_value('date', options)
        )
        time: datetime.time = self._convert_string_to_time(
            self._get_required_argument_value('time', options)
        )
        self.stdout.write(f'Converting {amount} {from_currency} to {to_currency} with {date} exchange rates...')
        api_client = ApiClient()

        try:
            response = api_client.convert_currency(
                amount=amount,
                source_currency=from_currency,
                destination_currency=to_currency,
                date=date,
                time=time
            )
            response_dict: dict = response.json()
        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            self.stdout.write(f'{e}')
            return

        if response.status_code == 200:
            self.stdout.write(f'{amount} {from_currency} == {response_dict.get("amount")} {to_currency} '
                              f'[exchange rates: {response_dict.get("exchange_rate_datetime")}]')

        currency_convertion_event_log_data: dict = {
            'api_request_amount': amount,
            'api_request_from_currency': from_currency,
            'api_request_to_currency': to_currency,
            'api_request_exchange_rate_datetime': datetime.datetime.combine(date, time),
            'api_response_converted_amount': response_dict.get('amount'),
            'api_response_exchange_rate_datetime': response_dict.get('exchange_rate_datetime'),
            'api_response_status_code': response.status_code,
            'api_response_body': response_dict,
        }

        serializer = CurrencyConvertionEventLogSerializer(data=currency_convertion_event_log_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            self.stdout.write(f'{e}')
            return

        serializer.save()

    @staticmethod
    def _get_required_argument_value(argument_name: str, options: dict) -> str:
        value = options.get(argument_name)
        if value is None:
            raise CommandError(f'Error: {argument_name} is required.')
        return value

    @staticmethod
    def _convert_string_to_decimal_amount(amount_str: str) -> Decimal:
        try:
            amount = Decimal(amount_str)
        except ValueError:
            raise CommandError(f'Error: Could not convert "{amount_str}" to Decimal,'
                               'make sure you provided a string amount in "0.00000" format.')
        return amount.quantize(Decimal(0.00000), rounding=ROUND_HALF_UP)

    @staticmethod
    def _convert_string_to_date(date_str: str) -> datetime.date:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise CommandError(f'Error: Could not convert "{date_str}" to datetime.date,'
                               'make sure you provided a string date in "%Y-%m-%d" format.')
        return date

    @staticmethod
    def _convert_string_to_time(time_str: str) -> datetime.time:
        try:
            time = datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise CommandError(f'Error: Could not convert "{time_str}" to datetime.time,'
                               'make sure you provided a string time in "%H:%M" format.')
        return time
