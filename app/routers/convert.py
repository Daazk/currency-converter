from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.api import get_currency_service
from app.schemas.currencies import ConvertQuery, ConvertResponse
from app.services.currency import CurrencyService
from app.services.exceptions import CurrencyNotFoundError

router = APIRouter(prefix="/api", tags=["Convert"])


@router.get("/convert", response_model=ConvertResponse)
def convert(
    query: Annotated[ConvertQuery, Query()],
    service: Annotated[CurrencyService, Depends(get_currency_service)],
) -> ConvertResponse:
    try:
        result = service.convert(query.from_currency, query.to_currency, query.amount)

    except CurrencyNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc

    return ConvertResponse.model_validate(result)
