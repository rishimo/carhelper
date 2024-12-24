from typing import Optional

from pydantic import EmailStr, Field, HttpUrl, model_validator
from pymongo.operations import IndexModel

from entities.base import CustomIDModel
from entities.location import Location
from entities.utils import create_hash


class Vendor(CustomIDModel):
    """
    Vendor model representing service providers and suppliers

    Attributes:
        name (str): Name of the vendor/business
        website (Optional[HttpUrl]): Vendor's website URL
        email (Optional[EmailStr]): Contact email address
        phone_number (Optional[str]): Contact phone number
        location (Location): Physical location of the vendor
    """

    name: str = Field(description="Vendor name")
    website: Optional[HttpUrl] = Field(description="Vendor website", default=None)
    email: Optional[EmailStr] = Field(description="Vendor email", default=None)
    phone_number: Optional[str] = Field(description="Vendor phone number", default=None)
    location: Location = Field(description="Vendor location")

    class Settings:
        name = "vendors"
        indexes = [
            IndexModel([("name", 1)]),  # TODO: support Atlas search
            IndexModel([("location.city", 1), ("location.state", 1)]),
        ]

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            location = data.get("location")
            loc_hash = create_hash(
                location.address,
                location.city,
                location.state,
            )
            data["id"] = f"VENDOR~{create_hash(data.get('name', ''), loc_hash)}"
        return data
