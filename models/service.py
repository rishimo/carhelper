from typing import List, Optional

from pendulum import today
from pydantic import Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime

from models.base import CustomIDModel
from models.enums import ServiceType
from models.file import File
from models.utils import create_hash
from models.vendor import Vendor


class ServiceItem(CustomIDModel):
    """
    Individual service item or task performed during a service visit

    Attributes:
        service_type (ServiceType): Type of service performed (e.g., MAINTENANCE)
        description (str): Detailed description of the service performed
        cost (float): Cost of the individual service item
        attachments (List[File]): Related documentation for the service item
    """

    service_type: ServiceType = Field(
        default=ServiceType.MAINTENANCE, description="Service type"
    )
    description: str = Field(description="Service description")
    cost: float = Field(description="Service cost")
    attachments: List[File] = Field(
        description="Documentation for the service", default_factory=list
    )

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            hash_value = create_hash(
                data.get("service_type", ""),
                data.get("description", ""),
                str(data.get("cost", "")),
            )
            data["id"] = f"SERVICE_ITEM~{hash_value}"
            return data
        return data


class Service(CustomIDModel):
    """
    Complete service record for a vehicle service visit

    Attributes:
        VIN (str): Vehicle Identification Number
        date (DateTime): Date and time of the service
        vendor_id (str): Service provider ID
        total_cost (float): Total cost of all service items
        items (List[ServiceItem]): List of individual service items performed
    """

    VIN: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor_id: str = Field(description="Service vendor ID")
    cost: Optional[float] = Field(
        description="Total cost of all service items", default=None
    )
    items: List[ServiceItem]

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            hash_value = create_hash(
                str(data.get("vendor", "")),
                str(data.get("date", "")),
                data.get("VIN", ""),
            )
            data["id"] = f"SERVICE~{hash_value}"
            return data
        return data

    @model_validator(mode="before")
    @classmethod
    def calculate_cost(cls, data: dict) -> dict:
        if data.get("cost") is None:
            data["cost"] = sum(item.cost for item in data.get("items", []))
        return data
