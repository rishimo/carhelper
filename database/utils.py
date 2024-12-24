from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models import User, Vehicle, Vendor
from server import CONFIG


async def init_db_handler():
    # init Motor client
    client = AsyncIOMotorClient(CONFIG.mongodb_connection_string)

    # init beanie
    await init_beanie(
        database=client.get_database(CONFIG.database_name),
        document_models=[User, Vehicle, Vendor],
    )
