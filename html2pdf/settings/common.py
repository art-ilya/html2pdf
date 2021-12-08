from typing import Optional

from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    DEBUG = True

    DATABASE_URI: Optional[str] = f"sqlite+aiosqlite:///html2pdf.db"
    # dramatiq has no async support, so define sync connection uri
    DATABASE_SYNC_URI: Optional[str] = f"sqlite:////workspaces/html2pdf/html2pdf.db"

    MESSAGE_BROKER_URI: Optional[str] = 'redis://redis_broker:6379/0'

    UPLOAD_DIR: Optional[str] = "./html2pdf/media/upload/"
    DOWNLOAD_DIR: Optional[str] = "./html2pdf/media/download/"
    BASE_DOWNLOAD_URL: Optional[str] = "http://localhost:8080/media"

    class Config:
        case_sensitive = True
