import os
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

import pytest

# Settings() требует переменные БД; тесты к БД не подключаются
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
os.environ.setdefault("POSTGRES_HOST", "localhost")


@dataclass
class FakeCurrency:
    code: str
    rate: Decimal
    rate_date: date


class FakeRepository:
    """Подменяет CurrencyRepository: хранит курсы в памяти."""

    def __init__(self, currencies: list[FakeCurrency] | None = None) -> None:
        self.currencies = {c.code: c for c in currencies or []}
        self.upserted: list = []
        self.upsert_calls = 0

    def get_by_code(self, code: str) -> FakeCurrency | None:
        return self.currencies.get(code)

    def upsert_many(self, rates) -> None:
        self.upsert_calls += 1
        self.upserted = list(rates)


@pytest.fixture
def repository() -> FakeRepository:
    return FakeRepository(
        [
            FakeCurrency("USD", Decimal("43.5"), date(2026, 10, 9)),
            FakeCurrency("EUR", Decimal("50.1385"), date(2026, 10, 9)),
            FakeCurrency("GBP", Decimal("59.1817"), date(2026, 10, 9)),
            FakeCurrency("VND", Decimal("0.0017349"), date(2026, 10, 8)),
        ]
    )
