from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URI: Optional[str] = "sqlite:///html2pdf.db"
    SQLITE_BASE_PATH: Optional[str] = "./"

    class Config:
        case_sensitive = True


config = Settings()