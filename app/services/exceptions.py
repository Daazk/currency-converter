class CurrencyNotFoundError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Валюта {code} не найдена")
