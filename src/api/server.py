import uvicorn
from fastapi import FastAPI

from src.api.routes import router as api_router
from src.core.config import settings
from src.db.session import engine
from src.db.utils import recreate_db_and_tables


async def on_startup_async(app: FastAPI):
    await recreate_db_and_tables(engine)
    yield


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        lifespan=on_startup_async  # Alterado para o nome da função assíncrona
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()


@app.get("/", tags=["health"])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )


if __name__ == '__main__':
    uvicorn.run('src.api.server:app', host="0.0.0.0", port=8000)
