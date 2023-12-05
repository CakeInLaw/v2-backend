from fastapi import FastAPI

from core.db import init_models
from core.settings import settings
from core.schemas import get_app_schema


app = FastAPI(
    debug=settings.app.DEBUG,
    version=settings.app.VERSION,
)


@app.get('/app/schema')
async def get_app_schema_route():
    return get_app_schema()


@app.on_event('startup')
async def on_startup():
    init_models()
