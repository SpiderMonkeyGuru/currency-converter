from django.contrib import admin

from converter.models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'currency_code',
        'rate',
        'exchange_currency',
        'exchange_rate_datetime',
        'created_at',
        'modified_at'
    )
    search_fields = (
        'id',
        'currency_code',
        'exchange_rate_datetime'
    )
admin.site.register(ExchangeRate, ExchangeRateAdmin)
