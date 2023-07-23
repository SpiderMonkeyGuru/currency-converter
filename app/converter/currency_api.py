import datetime
import logging
from typing import Optional

from rest_framework.exceptions import ValidationError

from app.currency_api import client as currency_api_client
from converter.serializers import LatestExchangeRatesSerializer

logger = logging.getLogger(__name__)


class CurrencyAPIClient:
    @staticmethod
    def retrieve_latest_exchange_rates(date: Optional[datetime.date] = None) -> dict:
        if date is None:
            result: dict = currency_api_client.latest()
        else:
            result: dict = currency_api_client.historical(date=date)

        serializer = LatestExchangeRatesSerializer(data=result)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(e)
            raise e

        return serializer.validated_data
