import pytest
from fastapi.testclient import TestClient

from app.dependencies.api import get_converter_service
from app.main import app
from app.services.currency_converter import CurrencyConverterService


@pytest.fixture
def client(repository):
    app.dependency_overrides[get_converter_service] = lambda: CurrencyConverterService(
        repository
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_convert(client):
    response = client.get(
        "/api/convert", params={"from_currency": "usd", "to_currency": "eur", "amount": 100}
    )

    assert response.status_code == 200
    assert response.json() == {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100.0,
        "result": 86.76,
        "rate": 0.867597,
        "rate_date": "2026-10-09",
    }


def test_unknown_currency_is_404(client):
    response = client.get(
        "/api/convert", params={"from_currency": "XAU", "to_currency": "USD", "amount": 1}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Валюта XAU не найдена"}


@pytest.mark.parametrize(
    "params",
    [
        {"from_currency": "US", "to_currency": "EUR", "amount": 1},
        {"from_currency": "USD", "to_currency": "EUR", "amount": 0},
        {"from_currency": "USD", "to_currency": "EUR", "amount": "abc"},
        {"from_currency": "USD", "to_currency": "EUR"},
    ],
)
def test_validation_error_is_422(client, params):
    response = client.get("/api/convert", params=params)

    assert response.status_code == 422
