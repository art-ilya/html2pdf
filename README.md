# html2pdf
Service for converting html to pdf

# Env variables
Set env variables in docker/common/dev.env

Defaults:

PYTHONUNBUFFERED=1

APP_CONFIG_NAME=dev

DATABASE_URI=sqlite+aiosqlite:///html2pdf.db

DATABASE_SYNC_URI=sqlite:///html2pdf.db


MESSAGE_BROKER_URI='redis://redis_broker:6379/0'

UPLOAD_DIR=/html2pdf/media/upload/

DOWNLOAD_DIR=/html2pdf/media/download/

BASE_DOWNLOAD_URL=http://localhost:8080/media

# Start and use
Run docker-compose up -d

Open in browser http://localhost:8080/docs and try it!

