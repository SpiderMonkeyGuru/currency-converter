# Generated by Django 4.2.3 on 2023-07-23 13:51

from decimal import Decimal
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("currency_code", models.CharField(max_length=3)),
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=5, default=Decimal("0"), max_digits=20
                    ),
                ),
                ("exchange_currency", models.CharField(default="USD", max_length=3)),
                ("exchange_rate_datetime", models.DateTimeField()),
            ],
            options={
                "ordering": ["-exchange_rate_datetime", "currency_code"],
            },
        ),
    ]
