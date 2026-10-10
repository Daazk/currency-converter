from sqlalchemy.orm import Session

from app.clients.nbu import NBUClient
from app.core.config import settings
from app.repositories.currency import CurrencyRepository
from app.services.currency import CurrencyService


def build_currency_service(session: Session) -> CurrencyService:
    return CurrencyService(
        nbu_client=NBUClient(settings.NBU_API_URL),
        repository=CurrencyRepository(session),
        excluded_codes=settings.EXCLUDED_CODES,
    )
