from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator
from pymongo.operations import IndexModel

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
    title: str = Field(
        description="File name specified by the user",
    )
    file: UploadFile = Field(
        description="File upload FastAPI object",
    )
    file_type: FileType = Field(
        description="File type",
    )
    description: Optional[str] = Field(description="File description")


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
    internal_filename: str = Field(
        description="File name, like an S3 object name",
    )
    description: Optional[str] = Field(description="File description")
    owner_user_id: str = Field(description="Owner of the file")
    entity_id: str = Field(description="Entity that the file is associated with")
    page_content: Optional[str] = Field(description="Page content of the file")

    class Settings:
        name = "files"
        indexes = [
            IndexModel([("owner_user_id", 1)]),
            IndexModel([("internal_filename", 1)]),
            IndexModel([("entity_id", 1)]),
            IndexModel([("type", 1)]),
        ]

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"FILE~{create_hash(data.get('internal_filename', ''))}"
        return data

    def check_owner(self, user_id: str) -> bool:
        """Check if the file is owned by the user."""
        return self.owner_user_id == user_id


class FileReturn(File):
    """
    File return model for file uploads
    """

    data: bytes = Field(description="File data")
