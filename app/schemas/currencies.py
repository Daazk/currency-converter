from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    field_validator,
)

CurrencyCode = Annotated[str, Field(pattern=r"^[A-Za-z]{3}$")]

# decimal внутри, число в JSON (по дефолту Pydantic v2 вернул бы строку "86.76")
JsonNumber = Annotated[Decimal, PlainSerializer(float, return_type=float)]


class NBURate(BaseModel):
    """Курс который отдаёт NBUClient: наш формат ответа НБУ."""

    code: str = Field(alias="cc")
    name: str = Field(alias="txt")
    rate: Decimal
    currency_date: date = Field(alias="exchangedate")

    @field_validator("currency_date", mode="before")
    @classmethod
    def parse_nbu_date(cls, value: str) -> date:
        return datetime.strptime(value, "%d.%m.%Y").date()


class ConvertQuery(BaseModel):
    from_currency: CurrencyCode
    to_currency: CurrencyCode
    amount: Decimal = Field(gt=0, le=Decimal("1e12"))

    @field_validator("from_currency", "to_currency", mode="before")
    @classmethod
    def to_upper(cls, value: str) -> str:
        return value.upper() if isinstance(value, str) else value


class ConvertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_currency: str
    to_currency: str
    amount: JsonNumber
    result: JsonNumber
    rate: JsonNumber
    rate_date: date | None
