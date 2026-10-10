from decimal import Decimal

import httpx
from pydantic import TypeAdapter, ValidationError

from app.schemas.currencies import NBURate


class NBUClientError(Exception):
    """НБУ недоступен или вернул данные не в ожидаемом формате."""


class NBUClient:
    """Получает курсы валют к UAH из открытого API НБУ. Больше ничего не делает."""

    _rates_adapter = TypeAdapter(list[NBURate])

    def __init__(self, url: str, timeout: float = 10.0) -> None:
        self._url = url
        self._timeout = timeout

    def fetch_rates(self) -> list[NBURate]:
        try:
            response = httpx.get(self._url, timeout=self._timeout)
            response.raise_for_status()
            # parse_float=Decimal: курс не проходит через float и не теряет точность
            data = response.json(parse_float=Decimal)
            return self._rates_adapter.validate_python(data)
        except httpx.HTTPError as exc:
            raise NBUClientError(f"Не удалось получить курсы НБУ: {exc}") from exc
        except (ValueError, ValidationError) as exc:
            raise NBUClientError(f"Некорректный ответ НБУ: {exc}") from exc
