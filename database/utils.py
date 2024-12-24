from typing import List

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db_handler(
    connection_string: str, database_name: str, document_models: List[Document]
):
    # init Motor client
    client = AsyncIOMotorClient(connection_string)

    # init beanie
    await init_beanie(
        database=client.get_database(database_name),
        document_models=document_models,
    )
