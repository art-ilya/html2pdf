from pathlib import Path
from uuid import UUID

from api.dependencies import get_db_session, upload_html_file
from crud.convert_request import crud
from fastapi import APIRouter, Depends, Form, HTTPException
from models.convert_request import SOURCE_TYPE
from pydantic import HttpUrl
from schemas.common import responses
from schemas.convert_request import ConvertRequest, ConvertRequestCreate
from sqlalchemy.ext.asyncio import AsyncSession
from workers.convert import convert_task

router = APIRouter(
    prefix="/convert_requests",
    tags=["convert_request"],
)


@router.post(
    "/url",
    status_code=201,
    response_model=ConvertRequest,
)
async def create_convert_request_url(
    url: HttpUrl = Form(...), db: AsyncSession = Depends(get_db_session)
):
    data_in = ConvertRequestCreate(source_type=SOURCE_TYPE.url, source=url)
    result = await crud.create_convert_request(db, data_in)
    await db.commit()
    
    task = convert_task.send(uid=str(result.id))
    
    return result


@router.post(
    "/file",
    status_code=201,
    response_model=ConvertRequest,
    responses={400: responses[400]},
)
async def create_convert_request_file(
    saved_html_path: Path = Depends(upload_html_file),
    db: AsyncSession = Depends(get_db_session),
):
    data_in = ConvertRequestCreate(
        source_type=SOURCE_TYPE.file, source=str(saved_html_path.name)
    )
    result = await crud.create_convert_request(db, data_in)
    await db.commit()

    task = convert_task.send(uid=str(result.id))
    
    return result


@router.get(
    "/{request_id}",
    response_model=ConvertRequest,
    responses={404: responses[404]},
)
async def get_convert_request(
    request_id: UUID, db: AsyncSession = Depends(get_db_session)
):
    result = await crud.get(db, id=request_id)
    if result is None:
        raise HTTPException(status_code=404)
    
    return result
