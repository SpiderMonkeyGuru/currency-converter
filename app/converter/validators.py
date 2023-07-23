from app.constants import ALLOWED_CURRENCIES
from converter.exceptions import InvalidCurrency


def is_currency_valid(currency_code: str) -> bool:
    if not currency_code.upper() in ALLOWED_CURRENCIES:
        raise InvalidCurrency(detail=f'Invalid currency: {currency_code.upper()}')
    return True


def are_provided_currencies_valid(from_currency: str, to_currency: str) -> bool:
    return True if is_currency_valid(from_currency) and is_currency_valid(to_currency) else False
