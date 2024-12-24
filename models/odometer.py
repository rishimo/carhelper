from typing import Optional

from pendulum import today
from pydantic import Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime

from models.base import CustomIDModel
from models.location import Location
from models.utils import create_hash


class OdometerReading(CustomIDModel):
    """
    Vehicle odometer reading record

    Attributes:
        VIN (str): Vehicle Identification Number
        date (DateTime): Date and time of the reading
        reading (float): Odometer value
        location (Optional[Location]): Location where reading was taken
    """

    VIN: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    reading: float
    location: Optional[Location] = Field(
        description="Odometer reading location", default=None
    )

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            hash_value = create_hash(
                data.get("VIN", ""),
                str(data.get("date", "")),
            )
            data["id"] = f"ODOMETER~{hash_value}"
            return data
        return data
