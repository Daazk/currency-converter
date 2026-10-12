from datetime import date
from decimal import Decimal

import pytest

from app.clients.nbu import NBUClientError
from app.schemas.currencies import NBURate
from app.services.currency_updater import CurrencyUpdaterService


def nbu_rate(code: str, rate: str) -> NBURate:
    return NBURate(cc=code, txt=code, rate=Decimal(rate), exchangedate="09.10.2026")


class FakeNBUClient:
    def __init__(self, rates: list[NBURate] | None = None, error: Exception | None = None) -> None:
        self._rates = rates or []
        self._error = error

    def fetch_rates(self) -> list[NBURate]:
        if self._error:
            raise self._error
        return self._rates


def test_saves_rates_except_excluded(repository):
    client = FakeNBUClient(
        [nbu_rate("USD", "43.5"), nbu_rate("XAU", "185061.47"), nbu_rate("XOF", "0.07")]
    )
    service = CurrencyUpdaterService(client, repository, excluded_codes=["XAU", "XDR"])

    count = service.update_rates()

    assert count == 2
    assert [r.code for r in repository.upserted] == ["USD", "XOF"]
    assert repository.upserted[0].currency_date == date(2026, 10, 9)


def test_nbu_error_does_not_touch_repository(repository):
    client = FakeNBUClient(error=NBUClientError("НБУ недоступен"))
    service = CurrencyUpdaterService(client, repository, excluded_codes=[])

    with pytest.raises(NBUClientError):
        service.update_rates()

    assert repository.upsert_calls == 0
