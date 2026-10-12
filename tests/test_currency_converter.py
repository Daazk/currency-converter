from datetime import date
from decimal import Decimal

import pytest

from app.services.currency_converter import (
    CurrencyConverterService,
    round_amount,
    round_significant,
)
from app.services.exceptions import CurrencyNotFoundError


@pytest.fixture
def service(repository) -> CurrencyConverterService:
    return CurrencyConverterService(repository)


def test_cross_rate(service):
    result = service.convert("USD", "EUR", Decimal("100"))

    assert result.result == Decimal("86.76")
    assert result.rate == Decimal("0.867597")
    assert result.rate_date == date(2026, 10, 9)


def test_result_uses_full_rates_not_rounded_cross_rate(service):
    result = service.convert("USD", "EUR", Decimal("1000000"))

    # 1000000 × 0.867597 дало бы 867597.00
    assert result.result == Decimal("867596.76")


def test_small_result_keeps_significant_digits(service):
    result = service.convert("VND", "GBP", Decimal("100"))

    assert result.result == Decimal("0.00293148")
    assert result.rate == Decimal("0.0000293148")


def test_rate_date_is_earliest(service):
    result = service.convert("VND", "USD", Decimal("1"))

    assert result.rate_date == date(2026, 10, 8)


def test_uah_rate_is_one(service):
    result = service.convert("UAH", "USD", Decimal("43.5"))

    assert result.result == Decimal("1.00")
    assert result.rate_date == date(2026, 10, 9)


def test_uah_to_uah_has_no_date(service):
    result = service.convert("UAH", "UAH", Decimal("5"))

    assert result.result == Decimal("5.00")
    assert result.rate == Decimal("1")
    assert result.rate_date is None


@pytest.mark.parametrize(
    ("from_currency", "to_currency", "missing"),
    [("XAU", "USD", "XAU"), ("USD", "ABC", "ABC"), ("ABC", "ABC", "ABC")],
)
def test_unknown_currency(service, from_currency, to_currency, missing):
    with pytest.raises(CurrencyNotFoundError) as exc_info:
        service.convert(from_currency, to_currency, Decimal("1"))

    assert exc_info.value.code == missing


def test_converter_does_not_write_to_repository(service, repository):
    service.convert("USD", "EUR", Decimal("100"))

    assert repository.upsert_calls == 0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("0.0000084654546"), Decimal("0.00000846545")),
        (Decimal("0.8675967569"), Decimal("0.867597")),
        (Decimal("0"), Decimal("0")),
    ],
)
def test_round_significant(value, expected):
    assert round_significant(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Decimal("86.755"), Decimal("86.76")),
        (Decimal("1"), Decimal("1.00")),
        (Decimal("0.0029314805"), Decimal("0.00293148")),
    ],
)
def test_round_amount(value, expected):
    assert round_amount(value) == expected
