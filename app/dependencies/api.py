from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.container import build_currency_service
from app.db.session import get_db
from app.services.currency import CurrencyService


def get_currency_service(db: Annotated[Session, Depends(get_db)]) -> CurrencyService:
    return build_currency_service(db)
