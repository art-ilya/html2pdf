from typing import Optional, Union
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl

from models.convert_request import CONVERT_STATUS, SOURCE_TYPE


class ConvertRequestBase(BaseModel):
    source_type: Optional[SOURCE_TYPE] = None
    source: Optional[Union[HttpUrl, str]] = None
    target: Optional[str] = None
    status: Optional[CONVERT_STATUS] = CONVERT_STATUS.pending


class ConvertRequestCreate(BaseModel):
    source_type: SOURCE_TYPE
    source: Union[HttpUrl, str]


class ConvertRequestUpdate(BaseModel):
    target: str
    status: CONVERT_STATUS


class ConvertRequestInDBBase(ConvertRequestBase):
    id: UUID
    created: datetime

    class Config:
        orm_mode = True


class ConvertRequestInDB(ConvertRequestInDBBase):
    pass


class ConvertRequest(BaseModel):
    id: UUID
    status: CONVERT_STATUS
    download_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True
