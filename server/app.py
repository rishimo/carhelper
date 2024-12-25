from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import init_db_handler

DESCRIPTION = """
A tool to help you manage your car's service history, expenses, mileage, and more.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services."""
    logger = getLogger(__name__)

    await init_db_handler()
    logger.info("DB connection successful")
    yield
    logger.info("Shutdown in progress...")


app = FastAPI(
    title="carHelper server",
    description=DESCRIPTION,
    version="0.1.0",
    contact={
        "name": "carHelper",
        "url": "https://rishimo.dev",
        "email": "hello@rishimo.dev",
    },
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
