from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from converter.views import CurrencyConverterViewSet

router = DefaultRouter()
router.register('currency-converter', CurrencyConverterViewSet, basename='currency-converter')


urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
