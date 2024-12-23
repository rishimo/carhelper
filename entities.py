from typing import List, Optional
from constants import Location, DocumentationType, ServiceType
from utils import create_hash

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.pendulum_dt import DateTime
from pendulum import today


class CustomIDModel(BaseModel):
    """
    Custom ID model for MongoDB that other entities inherit from
    """

    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


class Documentation(CustomIDModel):
    """
    Documentation model
    """

    documentation_type: DocumentationType = Field(
        default=DocumentationType.REPAIR_MANUAL, description="Documentation type"
    )
    uri: str = Field(
        description="Documentation URI, like an S3 item",
    )

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            return f"DOCUMENT~{create_hash(values['documentation_uri'])}"
        return v


class Vendor(CustomIDModel):
    """
    Vendor model
    """

    name: str = Field(description="Vendor name")
    website: Optional[str] = Field(description="Vendor website")
    email: Optional[str] = Field(description="Vendor email")
    phone_number: Optional[str] = Field(description="Vendor phone number")
    location: Location = Field(description="Vendor location")

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            loc_hash = create_hash(
                values["location"].street_address,
                values["location"].city,
                values["location"].state,
            )
            return f"VENDOR~{create_hash(values['name'], loc_hash)}"
        return v


class ServiceItem(CustomIDModel):
    service_type: ServiceType = Field(
        default=ServiceType.MAINTENANCE, description="Service type"
    )
    description: str = Field(description="Service description")
    cost: float = Field(description="Service cost")
    documentation: List[Documentation] = Field(
        description="Documentation for the service", default_factory=list
    )

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            return f"SERVICEITEM~{create_hash(values['service_type'], values['description'], str(values['cost']))}"
        return v


class Service(CustomIDModel):
    vin: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor: Vendor
    total_cost: float
    items: List[ServiceItem]

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            return f"SERVICE~{create_hash(values['vendor_ref'], str(values['date']), values['vin'])}"
        return v


class Fuel(CustomIDModel):
    vin: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor: Vendor
    fuel_type: str
    units: float
    price_per_unit: float
    total_cost: float


class OdometerReading(CustomIDModel):
    vin: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    location: Location
    reading: float

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            return f"ODOMETER~{create_hash(values['vin'], str(values['date']))}"
        return v


class Vehicle(CustomIDModel):
    vin: str = Field(description="Vehicle VIN")
    make: str
    model: str
    year: int
    color: str
    odometer_records: List[OdometerReading]
    service_records: List[Service]
    fuel_records: List[Fuel]
    documentation: List[Documentation]

    def current_mileage(self) -> float:
        return self.odometer_records[-1].reading

    @field_validator("id", mode="before")
    @classmethod
    def generate_id(cls, v: str | None, values: dict) -> str:
        if v is None:
            return f"VEHICLE~{values['vin']}"
        return v
