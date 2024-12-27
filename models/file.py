from typing import Optional

from pydantic import Field, model_validator

from models.base import CustomIDModel
from models.enums import FileType
from models.utils import create_hash


class File(CustomIDModel):
    """
    File model for storing file metadata and references

    Attributes:
        documentation_type (DocumentationType): Type of documentation (e.g., REPAIR_MANUAL)
        title (str): Title of the documentation
        filename (str): filename of the file (e.g., S3 object name)
        description (Optional[str]): Optional detailed description of the document
    """

    type: FileType = Field(default=FileType.REPAIR_MANUAL, description="File type")
    title: str = Field(description="File title")
    filename: str = Field(
        description="File name, like an S3 object name",
    )
    description: Optional[str] = Field(description="File description")

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"FILE~{create_hash(data.get('filename', ''))}"
        return data
