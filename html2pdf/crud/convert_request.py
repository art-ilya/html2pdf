from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from models.convert_request import ConvertRequestModel
from schemas.convert_request import ConvertRequestCreate
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CRUDConvertRequest:
    async def create_convert_request(
        self, db: AsyncSession, obj_in: ConvertRequestCreate
    ) -> ConvertRequestModel:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = ConvertRequestModel(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        return db_obj

    async def get(self, db: AsyncSession, id: str) -> Optional[ConvertRequestModel]:
        stmt = select(ConvertRequestModel).where(ConvertRequestModel.id == id)
        result = await db.execute(stmt)
        db_obj = result.scalars().first()
        return db_obj


crud = CRUDConvertRequest()
