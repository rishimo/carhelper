from database.collections import COLLECTIONS

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)


class DatabaseManager:
    """
    Manages MongoDB database setup, including collections and indexes
    """

    def __init__(self, connection_string: str, database_name: str):
        """
        Initialize database connection and setup

        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[database_name]

    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        """
        Get a collection by name

        Args:
            name: Name of the collection

        Returns:
            MongoDB collection
        """
        return self.db[name]

    async def setup_collections(self) -> None:
        """
        Creates collections and ensures indexes are properly set up
        """
        for collection_name, config in COLLECTIONS.items():
            collection = self.db[collection_name]

            # Create or update indexes
            if "indexes" in config:
                existing_indexes = set()
                async for index in collection.list_indexes():
                    existing_indexes.add(index["name"])

                for index in config["indexes"]:
                    index_name = index.document.get("name")
                    if index_name not in existing_indexes:
                        await collection.create_indexes([index])

    async def reset_collections(self) -> None:
        """
        Drops and recreates all collections with their indexes.
        WARNING: This will delete all data!
        """
        for collection_name in COLLECTIONS:
            if collection_name in await self.db.list_collection_names():
                await self.db[collection_name].drop()

        await self.setup_collections()

    def get_database(self) -> AsyncIOMotorDatabase:
        """
        Get the database instance

        Returns:
            MongoDB database
        """
        return self.db

    def close(self) -> None:
        """
        Close the database connection
        """
        self.client.close()
