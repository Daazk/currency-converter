from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    NBU_API_URL: str = (
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    EXCLUDED_CODES: list[str] = ["XAU", "XAG", "XPT", "XPD", "XDR"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def DATABASE_URL(self) -> URL:
        # URL.create сам экранирует спецсимволы в пароле
        return URL.create(
            "postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings()
