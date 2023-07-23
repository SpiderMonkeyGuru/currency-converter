import datetime

from django.core.management.base import BaseCommand, CommandError

from converter.services import retrieve_latest_exchange_rates


class Command(BaseCommand):
    help = 'This commands helps you populate the DB with historical exchange rates for a given dates'
    name = 'download_rates'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Date of the exchange rates to download')

    def handle(self, *args, **options):
        date: datetime.date = self._convert_string_to_date(
            self._get_required_argument_value('date', options)
        )
        self.stdout.write(f'Downloading exchange rates from: {date}')
        try:
            retrieve_latest_exchange_rates(date)
        except Exception as e:
            self.stdout.write(f'{e}')

    @staticmethod
    def _get_required_argument_value(argument_name: str, options: dict) -> str:
        value = options.get(argument_name)
        if value is None:
            raise CommandError(f'Error: {argument_name} is required.')
        return value

    @staticmethod
    def _convert_string_to_date(date_str: str) -> datetime.date:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise CommandError(f'Error: Could not convert "{date_str}" to datetime.date,'
                               'make sure provided a string date in "%Y-%m-%d" format.')
        return date
