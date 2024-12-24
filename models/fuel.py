from typing import Optional

from pendulum import today
from pydantic import Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime

from models.base import CustomIDModel
from models.enums import FuelType
from models.utils import create_hash


class Fuel(CustomIDModel):
    """
    Fuel purchase record

    Attributes:
        VIN (str): Vehicle Identification Number
        date (DateTime): Date and time of fuel purchase
        vendor_id (str): Fuel vendor ID
        fuel_type (FuelType): Type of fuel purchased
        units (float): Amount of fuel purchased
        price_per_unit (float): Cost per unit of fuel
        total_cost (float): Total cost of the fuel purchase
    """

    VIN: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor_id: str = Field(description="Fuel vendor ID")
    fuel_type: FuelType = Field(description="Type of fuel purchased")
    units: float = Field(description="Units of fuel purchased")
    price_per_unit: float = Field(description="Price per unit of fuel")
    cost: Optional[float] = Field(
        description="Total cost of the fuel purchase", default=None
    )

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = (
                f"FUEL~{create_hash(data.get('VIN', ''), str(data.get('date', '')))}"
            )
            return data
        return data

    @model_validator(mode="before")
    @classmethod
    def calculate_cp(cls, data: dict) -> dict:
        if data.get("cost") is None:
            data["cost"] = data.get("units") * data.get("price_per_unit")
        return data
