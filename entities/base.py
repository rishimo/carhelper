from pydantic import BaseModel, Field


class CustomIDModel(BaseModel):
    id: str = Field(alias="_id")

    model_config = {
        "populate_by_name": True,
    }
