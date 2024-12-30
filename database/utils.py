from enum import Enum
from typing import Type

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models import File, User, Vehicle, Vendor
from server import CONFIG


class EntityTypeToString(str, Enum):
    """
    Entity type enum
    """

    VEHICLE = "VEHICLE"
    VENDOR = "VENDOR"
    FILE = "FILE"
    USER = "USER"


class EntityTypeToClass(str, Enum):
    """
    Entity type to class mapping
    """

    VEHICLE = Vehicle
    VENDOR = Vendor
    FILE = File
    USER = User


def entity_id_to_type(entity_id: str) -> Type[Vehicle | Vendor | File | User]:
    """
    Convert entity ID to entity type
    """
    return EntityTypeToClass(entity_id.split("~")[0])


def entity_id_to_type_string(entity_id: str) -> str:
    """
    Convert entity ID to entity type string
    """
    return EntityTypeToString(entity_id.split("~")[0])


async def init_db_handler():
    # init Motor client
    client = AsyncIOMotorClient(CONFIG.mongodb_connection_string)

    # init beanie
    await init_beanie(
        database=client.get_database(CONFIG.database_name),
        document_models=[File, User, Vehicle, Vendor],
    )


async def add_file_to_entity_by_id(file_id: str, entity_id: str) -> bool:
    entity_type = entity_id_to_type(entity_id)
    entity = await entity_type.find_by_id(entity_id)

    if not entity:
        return False

    entity.file_ids.append(file_id)
    await entity.save()

    return True


async def delete_file_from_entity_by_id(file_id: str, entity_id: str) -> bool:
    entity_type = entity_id_to_type(entity_id)
    entity = await entity_type.find_by_id(entity_id)

    if not entity:
        return False

    entity.file_ids.remove(file_id)
    await entity.save()
    return True
