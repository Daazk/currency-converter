from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.container import build_converter_service
from app.db.session import get_db
from app.services.currency_converter import CurrencyConverterService


def get_converter_service(db: Annotated[Session, Depends(get_db)]) -> CurrencyConverterService:
    return build_converter_service(db)
