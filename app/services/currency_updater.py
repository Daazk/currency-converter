from app.clients.nbu import NBUClient
from app.repositories.currency import CurrencyRepository


class CurrencyUpdaterService:
    def __init__(
        self,
        nbu_client: NBUClient,
        repository: CurrencyRepository,
        excluded_codes: list[str],
    ) -> None:

        self._nbu_client = nbu_client
        self._repository = repository
        self._excluded = set(excluded_codes)

    def update_rates(self) -> int:
        rates = self._nbu_client.fetch_rates()
        currencies = [r for r in rates if r.code not in self._excluded]

        self._repository.upsert_many(currencies)
        return len(currencies)
