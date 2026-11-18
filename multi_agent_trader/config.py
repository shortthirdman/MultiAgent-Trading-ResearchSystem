from pydantic import SecretStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class TraderConfig(BaseSettings):
    EODHD_API_KEY: SecretStr
    START_DATE: str = "2020-01-01"
    END_DATE: str = "2020-01-01"
    DEFAULT_TICKERS: list[str] = ["SPY", "QQQ", "IWM", "XLE", "XLF", "XLK", "XLV", "XLP", "XLY"]

settings = TraderConfig()