from typing import Optional

from pydantic import Field, model_validator

from models.base import CustomIDModel
from models.enums import DocumentationType
from models.utils import create_hash


class Documentation(CustomIDModel):
    """
    Documentation model for storing document metadata and references

    Attributes:
        documentation_type (DocumentationType): Type of documentation (e.g., REPAIR_MANUAL)
        title (str): Title of the documentation
        uri (str): URI reference to the document location (e.g., S3 path)
        description (Optional[str]): Optional detailed description of the document
    """

    documentation_type: DocumentationType = Field(
        default=DocumentationType.REPAIR_MANUAL, description="Documentation type"
    )
    title: str = Field(description="Documentation title")
    uri: str = Field(
        description="Documentation URI, like an S3 item",
    )
    description: Optional[str] = Field(description="Documentation description")

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"DOCUMENT~{create_hash(data.get('uri', ''))}"
        return data
