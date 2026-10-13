
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Stock Trading System"
    app_env: str = "development"

    api_host: str = "127.0.0.1"
    api_port: int = 8000

    frontend_url: str = "http://localhost:5173"

    groq_api_key: str
    groq_model_name: str = "openai/gpt-oss-120b"
    serper_api_key: str = ""

    csv_scan_roots: str = r"C:\\,D:\\,E:\\"
    csv_file_pattern: str = "stock_Analysis*.csv"

    max_csv_rows: int = 5000
    max_file_size_mb: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_scan_roots(self):
        return [
            path.strip()
            for path in self.csv_scan_roots.split(",")
            if path.strip()
        ]


@lru_cache
def get_settings():
    return Settings()
