from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="html2pdf",
        description="Service for converting html to pdf",
        redoc_url=None,
    )

    return app