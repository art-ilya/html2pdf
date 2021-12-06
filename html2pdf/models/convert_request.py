import uuid
from datetime import datetime
from enum import Enum

import sqlalchemy as sa
from db import GUID, Base


class CONVERT_STATUS(str, Enum):
    pending = "pending"
    success = "success"
    failure = "failure"


class SOURCE_TYPE(str, Enum):
    url = "url"
    file = "file"


class ConvertRequestModel(Base):
    __tablename__ = "convert_request"
    id = sa.Column(GUID, primary_key=True, default=uuid.uuid4)
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    source_type = sa.Column(sa.String(10), nullable=False)
    source = sa.Column(sa.String(2083), nullable=False)
    target = sa.Column(sa.String(250))
    status = sa.Column(sa.String(10), nullable=False, default=CONVERT_STATUS.pending)

    def __repr__(self):
        return f"ConvertRequestModel(id={self.id})"


""" class ConvertRequestModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created: datetime = Field(default_factory=datetime.utcnow)
    source_type: SOURCE_TYPE
    source: Union[HttpUrl, str]
    target: Optional[str] = None
    status: CONVERT_STATUS = CONVERT_STATUS.pending """
