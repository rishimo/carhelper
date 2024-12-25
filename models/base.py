from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field


class CustomIDModel(Document):
    id: str = Field(description="Document ID", alias="_id")

    class Settings:
        populate_by_name = True
        keep_nulls = False

    @classmethod
    async def find_by_id(cls, id: str) -> Optional["CustomIDModel"]:
        """Find a document by id."""
        return await cls.find_one(cls.id == id)

    async def update_instance(self, input: BaseModel) -> bool:
        """Update the instance with the given input."""
        fields = input.model_dump(exclude_unset=True)
        for key, value in fields.items():
            setattr(self, key, value)
        await self.save()
        return True
