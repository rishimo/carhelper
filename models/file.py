from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator

from models.base import CustomIDModel
from models.enums import FileType
from models.utils import create_hash


class FileUpload(BaseModel):
    """
    File upload model for user file uploads
    """

    entity_id: str = Field(
        description="Entity that the file is associated with",
    )
    user_filename: str = Field(
        description="File name specified by the user",
    )
    file: UploadFile = Field(
        description="File upload FastAPI object",
    )
    file_type: FileType = Field(
        description="File type",
    )


class File(CustomIDModel):
    """
    File model for storing file metadata and references

    Attributes:
        documentation_type (DocumentationType): Type of documentation (e.g., REPAIR_MANUAL)
        title (str): Title of the documentation
        filename (str): filename of the file (e.g., S3 object name)
        description (Optional[str]): Optional detailed description of the document
    """

    type: FileType = Field(default=FileType.RECEIPT, description="File type")
    title: str = Field(description="File title")
    user_filename: str = Field(
        description="File name specified by the user",
    )
    internal_filename: str = Field(
        description="File name, like an S3 object name",
    )
    description: Optional[str] = Field(description="File description")
    owner: str = Field(description="Owner of the file")

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"FILE~{create_hash(data.get('internal_filename', ''))}"
        return data

    def check_owner(self, username: str) -> bool:
        """Check if the file is owned by the user."""
        return self.owner == username
