from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Currency(Base):
    __tablename__ = "currencies"
    __table_args__ = (CheckConstraint("rate > 0", name="ck_currencies_rate_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    rate: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    rate_date: Mapped[date] = mapped_column(Date)
