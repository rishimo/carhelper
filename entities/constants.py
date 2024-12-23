from enum import Enum
from typing import Optional, Tuple

from pydantic import BaseModel, Field


class DocumentationType(str, Enum):
    """
    Documentation type enum
    """

    REPAIR_MANUAL = "REPAIR_MANUAL"
    SERVICE_RECORD = "SERVICE_RECORD"
    OWNER_MANUAL = "OWNER_MANUAL"
    SERVICE_INTERVAL = "SERVICE_INTERVAL"
    WARRANTY_DOCUMENTATION = "WARRANTY_DOCUMENTATION"


class ServiceType(str, Enum):
    """
    Service type enum
    """

    MAINTENANCE = "MAINTENANCE"
    REPAIR = "REPAIR"
    MODIFICATION = "MODIFICATION"
    INSPECTION = "INSPECTION"


class FuelType(str, Enum):
    """
    Fuel type enum
    """

    REGULAR = "Regular"
    PREMIUM = "Premium"
    DIESEL = "Diesel"
    ELECTRICITY = "Electricity"
    OTHER = "Other"


class Location(BaseModel):
    """
    Location model
    """

    address: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float] = Field(
        description="Latitude of the location", default=None
    )
    longitude: Optional[float] = Field(
        description="Longitude of the location", default=None
    )

    def get_coordinates(self) -> Tuple[float, float]:
        if self.latitude is None or self.longitude is None:
            raise ValueError("Latitude and longitude are required")
        # TODO: Get coordinates from Google Maps API
        return self.latitude, self.longitude
