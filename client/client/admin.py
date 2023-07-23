from django.contrib import admin

from .models import CurrencyConvertionEventLog


class CurrencyConvertionEventLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'api_request_amount',
        'api_request_from_currency',
        'api_response_converted_amount',
        'api_request_to_currency',
        'api_request_exchange_rate_datetime',
        'api_response_status_code',
        'created_at'
    )
    search_fields = (
        'id',
        'api_request_amount',
        'api_request_from_currency',
        'api_response_converted_amount',
        'api_request_to_currency',
        'api_request_exchange_rate_datetime',
        'api_response_status_code',
        'created_at'
    )

admin.site.register(CurrencyConvertionEventLog, CurrencyConvertionEventLogAdmin)
