from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from app.repositories.currency import CurrencyRepository
from app.services.exceptions import CurrencyNotFoundError

BASE_CURRENCY = "UAH"


def round_significant(value: Decimal, digits: int = 6) -> Decimal:
    """Округляет до 'digits' значущих цифр: 0.0000084654546 → 0.00000846545."""

    if value == 0:
        return value

    exponent = value.adjusted() - digits + 1
    return value.quantize(Decimal(1).scaleb(exponent), rounding=ROUND_HALF_UP)


def round_amount(value: Decimal) -> Decimal:
    """Сумма: 2 знака после запятой, а меньше 1 - 6 значащих цифр."""

    if abs(value) >= 1:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return round_significant(value)


@dataclass(frozen=True)
class ConvertResult:
    from_currency: str
    to_currency: str
    amount: Decimal
    result: Decimal
    rate: Decimal
    rate_date: date | None


class CurrencyConverterService:
    def __init__(self, repository: CurrencyRepository) -> None:
        self._repository = repository

    def convert(
        self, from_currency: str, to_currency: str, amount: Decimal
    ) -> ConvertResult:
        from_rate, from_date = self._get_rate(from_currency)
        to_rate, to_date = self._get_rate(to_currency)

        dates = [d for d in (from_date, to_date) if d is not None]

        return ConvertResult(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            result=round_amount(amount * from_rate / to_rate),
            rate=round_significant(from_rate / to_rate),
            rate_date=min(dates) if dates else None,
        )

    def _get_rate(self, code: str) -> tuple[Decimal, date | None]:
        if code == BASE_CURRENCY:
            return Decimal(1), None

        currency = self._repository.get_by_code(code)
        if currency is None:
            raise CurrencyNotFoundError(code)

        return currency.rate, currency.rate_date
