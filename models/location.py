from typing import Optional, Tuple

from pydantic import BaseModel, Field


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
