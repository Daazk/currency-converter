from sqlalchemy.orm import Session

from app.clients.nbu import NBUClient
from app.core.config import settings
from app.repositories.currency import CurrencyRepository
from app.services.currency_converter import CurrencyConverterService
from app.services.currency_updater import CurrencyUpdaterService


def build_converter_service(session: Session) -> CurrencyConverterService:
    return CurrencyConverterService(CurrencyRepository(session))


def build_updater_service(session: Session) -> CurrencyUpdaterService:
    return CurrencyUpdaterService(
        nbu_client=NBUClient(settings.NBU_API_URL),
        repository=CurrencyRepository(session),
        excluded_codes=settings.EXCLUDED_CODES,
    )
