from enum import Enum
from typing import Optional, Tuple
from utils import create_hash

from pydantic import BaseModel, field_validator
from pyvin.utils import validate_vin


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


class Location(BaseModel):
    """
    Location model
    """

    street_address: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]

    def get_coordinates(self) -> Tuple[float, float]:
        if self.latitude is None or self.longitude is None:
            raise ValueError("Latitude and longitude are required")
        # TODO: Get coordinates from Google Maps API
        return self.latitude, self.longitude
