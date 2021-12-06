from typing import Optional

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    DEBUG = True

    SQLITE_DB_NAME: Optional[str] = "html2pdf.db"
    DATABASE_URI: Optional[str] = f"sqlite+aiosqlite:///{SQLITE_DB_NAME}"

    UPLOAD_DIR: Optional[str] = "./html2pdf/media/upload/"
    DOWNLOAD_DIR: Optional[str] = "./html2pdf/media/download/"
    BASE_DOWNLOAD_URL: Optional[str] = "http://localhost:8000/download"

    class Config:
        case_sensitive = True
