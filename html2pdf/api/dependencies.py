import pathlib
import uuid
from db import async_session
from fastapi import Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.storage import LocalFileStorage
from settings import config


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def validate_html_file(html: UploadFile = File(...)) -> UploadFile:
    if html.content_type != "text/html":
        raise HTTPException(status_code=400, detail="Invalid file type")
    return html


async def upload_html_file(
    html: UploadFile = Depends(validate_html_file),
) -> pathlib.Path:
    file_ext = pathlib.Path(html.filename).suffix
    uniq_filename = f"{uuid.uuid4()}{file_ext}"
    local_storage = LocalFileStorage(base_path=config.UPLOAD_DIR)
    saved_file_path = await local_storage.save_file_async(
        in_file=html, uniq_filename=uniq_filename
    )
    return saved_file_path
