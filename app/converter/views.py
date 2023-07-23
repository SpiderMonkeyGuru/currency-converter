import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_api_key.permissions import HasAPIKey

from converter.serializers import ExchangeCurrenciesSerializer
from converter.services import exchange_currencies

logger = logging.getLogger(__name__)


class CurrencyConverterViewSet(GenericViewSet):
    @action(methods=['GET'], detail=False, url_name='convert', permission_classes=[HasAPIKey])
    def convert(self, request: Request) -> Response:
        serializer = ExchangeCurrenciesSerializer(data=request.query_params)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.error(e)
            raise e
        response_data: dict = exchange_currencies(**serializer.validated_data)
        return Response(data=response_data, status=status.HTTP_200_OK)
