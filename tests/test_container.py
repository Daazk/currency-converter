from unittest.mock import MagicMock

from app.clients.nbu import NBUClient
from app.dependencies import container
from app.services.currency_converter import CurrencyConverterService
from app.services.currency_updater import CurrencyUpdaterService


def test_converter_is_built_without_nbu_client(monkeypatch):
    nbu_client = MagicMock(spec=NBUClient)
    monkeypatch.setattr(container, "NBUClient", nbu_client)

    service = container.build_converter_service(MagicMock())

    assert isinstance(service, CurrencyConverterService)
    nbu_client.assert_not_called()


def test_updater_is_built_with_nbu_client(monkeypatch):
    nbu_client = MagicMock(spec=NBUClient)
    monkeypatch.setattr(container, "NBUClient", nbu_client)

    service = container.build_updater_service(MagicMock())

    assert isinstance(service, CurrencyUpdaterService)
    nbu_client.assert_called_once()
