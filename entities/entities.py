from typing import List, Optional
from entities.constants import Location, DocumentationType, ServiceType, FuelType
from entities.utils import create_hash

from pydantic import BaseModel, Field, model_validator, model_validator
from pydantic_extra_types.pendulum_dt import DateTime
from pendulum import today


class CustomIDModel(BaseModel):
    """
    Custom ID model for MongoDB that other entities inherit from

    Attributes:
        id (str): MongoDB document identifier, aliased as '_id'
    """

    id: str = Field(alias="_id")

    model_config = {
        "populate_by_name": True,
    }


class Documentation(CustomIDModel):
    """
    Documentation model for storing document metadata and references

    Attributes:
        documentation_type (DocumentationType): Type of documentation (e.g., REPAIR_MANUAL)
        title (str): Title of the documentation
        uri (str): URI reference to the document location (e.g., S3 path)
        description (Optional[str]): Optional detailed description of the document
    """

    documentation_type: DocumentationType = Field(
        default=DocumentationType.REPAIR_MANUAL, description="Documentation type"
    )
    title: str = Field(description="Documentation title")
    uri: str = Field(
        description="Documentation URI, like an S3 item",
    )
    description: Optional[str] = Field(description="Documentation description")

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"DOCUMENT~{create_hash(data.get('uri', ''))}"
        return data


class Vendor(CustomIDModel):
    """
    Vendor model representing service providers and suppliers

    Attributes:
        name (str): Name of the vendor/business
        website (Optional[str]): Vendor's website URL
        email (Optional[str]): Contact email address
        phone_number (Optional[str]): Contact phone number
        location (Location): Physical location of the vendor
    """

    name: str = Field(description="Vendor name")
    website: Optional[str] = Field(description="Vendor website", default=None)
    email: Optional[str] = Field(description="Vendor email", default=None)
    phone_number: Optional[str] = Field(description="Vendor phone number", default=None)
    location: Location = Field(description="Vendor location")

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


class ServiceItem(CustomIDModel):
    """
    Individual service item or task performed during a service visit

    Attributes:
        service_type (ServiceType): Type of service performed (e.g., MAINTENANCE)
        description (str): Detailed description of the service performed
        cost (float): Cost of the individual service item
        documentation (List[Documentation]): Related documentation for the service item
    """

    service_type: ServiceType = Field(
        default=ServiceType.MAINTENANCE, description="Service type"
    )
    description: str = Field(description="Service description")
    cost: float = Field(description="Service cost")
    documentation: List[Documentation] = Field(
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
        vendor (Vendor): Service provider information
        total_cost (float): Total cost of all service items
        items (List[ServiceItem]): List of individual service items performed
    """

    VIN: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor: Vendor
    total_cost: Optional[float] = Field(
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
    def calculate_total_cost(cls, data: dict) -> dict:
        if data.get("total_cost") is None:
            data["total_cost"] = sum(item.cost for item in data.get("items", []))
        return data


class Fuel(CustomIDModel):
    """
    Fuel purchase record

    Attributes:
        VIN (str): Vehicle Identification Number
        date (DateTime): Date and time of fuel purchase
        vendor (Vendor): Fuel vendor information
        fuel_type (FuelType): Type of fuel purchased
        units (float): Amount of fuel purchased
        price_per_unit (float): Cost per unit of fuel
        total_cost (float): Total cost of the fuel purchase
    """

    VIN: str = Field(description="Vehicle VIN")
    date: DateTime = Field(default_factory=today)
    vendor: Vendor = Field(description="Fuel vendor")
    fuel_type: FuelType = Field(description="Type of fuel purchased")
    units: float = Field(description="Units of fuel purchased")
    price_per_unit: float = Field(description="Price per unit of fuel")
    total_cost: Optional[float] = Field(
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
    def calculate_total_cost(cls, data: dict) -> dict:
        if data.get("total_cost") is None:
            data["total_cost"] = data.get("units") * data.get("price_per_unit")
        return data


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


class Vehicle(CustomIDModel):
    """
    Primary vehicle record containing all vehicle-related information

    Attributes:
        VIN (str): Vehicle Identification Number
        make (str): Vehicle manufacturer
        model (str): Vehicle model name
        year (int): Vehicle manufacturing year
        color (Optional[str]): Vehicle color, defaults to "NOT_SET"
        odometer_records (Optional[List[OdometerReading]]): History of odometer readings
        service_records (Optional[List[Service]]): History of service visits
        fuel_records (Optional[List[Fuel]]): History of fuel purchases
        documentation (Optional[List[Documentation]]): Vehicle-related documentation
    """

    VIN: str = Field(description="Vehicle VIN")
    make: str = Field(description="Vehicle make")
    model: str = Field(description="Vehicle model")
    year: int = Field(description="Vehicle year")
    color: Optional[str] = Field(description="Vehicle color", default="NOT_SET")
    odometer_records: Optional[List[OdometerReading]] = Field(
        default_factory=list, description="Odometer records"
    )
    service_records: Optional[List[Service]] = Field(
        default_factory=list, description="Service records"
    )
    fuel_records: Optional[List[Fuel]] = Field(
        default_factory=list, description="Fuel records"
    )
    documentation: Optional[List[Documentation]] = Field(
        default_factory=list, description="Documentation"
    )

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"VEHICLE~{data.get('VIN')}"
            return data
        return data

    def add_odometer_record(self, odometer_record: OdometerReading):
        if odometer_record.VIN != self.VIN:
            raise ValueError("Odometer record VIN does not match vehicle VIN")
        self.odometer_records.append(odometer_record)

    def current_mileage(self) -> float:
        if not self.odometer_records:
            raise ValueError("No odometer records found")
        return self.odometer_records[-1].reading

    def add_service_record(self, service_record: Service):
        if service_record.VIN != self.VIN:
            raise ValueError("Service record VIN does not match vehicle VIN")
        self.service_records.append(service_record)

    def add_fuel_record(self, fuel_record: Fuel):
        if fuel_record.VIN != self.VIN:
            raise ValueError("Fuel record VIN does not match vehicle VIN")
        self.fuel_records.append(fuel_record)

    def add_documentation(self, documentation: Documentation):
        self.documentation.append(documentation)
