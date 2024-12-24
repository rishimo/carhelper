from beanie import Document
from pydantic import Field


class CustomIDModel(Document):
    id: str = Field(description="Document ID", alias="_id")

    model_config = {
        "populate_by_name": True,
    }
