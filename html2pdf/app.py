from fastapi import FastAPI
from api.v1 import api
from settings import config
from db.init_db import try_init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title="html2pdf",
        description="Service for converting html to pdf",
        redoc_url=None,
    )

    app.include_router(api.router)

    @app.on_event("startup")
    async def startup():
        await try_init_db()

    return app
