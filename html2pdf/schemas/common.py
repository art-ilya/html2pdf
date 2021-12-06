from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


responses = {
    404: {"model": HTTPError, "description": "Item not found"},
    400: {"model": HTTPError, "description": "Bad request"},
}
