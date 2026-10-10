from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.currencies import Currency
from app.schemas.currencies import NBURate


class CurrencyRepository:
    """Работа с таблицей currencies. Никакой бизнес-логики."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_code(self, code: str) -> Currency | None:
        return self._session.scalar(select(Currency).where(Currency.code == code))

    def upsert_many(self, rates: Iterable[NBURate]) -> None:
        values = [
            {
                "code": rate.code,
                "name": rate.name,
                "rate": rate.rate,
                "rate_date": rate.currency_date,
            }
            for rate in rates
        ]

        if not values:
            return

        stmt = insert(Currency).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=["code"],
            set_={
                "name": stmt.excluded.name,
                "rate": stmt.excluded.rate,
                "rate_date": stmt.excluded.rate_date,
            },
        )

        try:
            self._session.execute(stmt)
            self._session.commit()

        except Exception:
            self._session.rollback()
            raise
