from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from config import db_helper
from api import router as api_router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
