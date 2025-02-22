from typing import List, Optional

from pydantic import Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime
from pymongo.operations import IndexModel

from models.base import CustomIDModel
from models.expense import Expense
from models.file import File
from models.fuel import Fuel
from models.odometer import OdometerReading
from models.service import Service


class Vehicle(CustomIDModel):
    """
    Primary vehicle record containing all vehicle-related information

    Attributes:
        VIN (str): Vehicle Identification Number
        make (str): Vehicle manufacturer
        model (str): Vehicle model name
        year (int): Vehicle manufacturing year
        color (Optional[str]): Vehicle color, defaults to "NOT_SET"
        owner_id (Optional[str]): Vehicle owner ID
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
    owner_id: Optional[str] = Field(description="Vehicle owner ID", default=None)
    purchase_date: Optional[DateTime] = Field(
        description="Vehicle purchase date", default=None
    )
    purchase_price: Optional[float] = Field(
        description="Vehicle purchase price", default=None
    )
    odometer_records: Optional[List[OdometerReading]] = Field(
        default_factory=list, description="Odometer records"
    )
    service_records: Optional[List[Service]] = Field(
        default_factory=list, description="Service records"
    )
    fuel_records: Optional[List[Fuel]] = Field(
        default_factory=list, description="Fuel records"
    )
    expenses: Optional[List[Expense]] = Field(
        default_factory=list, description="Expenses"
    )
    file_ids: Optional[List[str]] = Field(default_factory=list, description="File IDs")

    class Settings:
        name = "vehicles"
        indexes = [
            IndexModel([("owner_id", 1)]),
            IndexModel([("service_records.date", -1)]),
            IndexModel([("fuel_records.date", -1)]),
            IndexModel([("odometer_records.date", -1)]),
            IndexModel([("make", 1), ("model", 1), ("year", 1)]),
            IndexModel([("file_ids", 1)]),
        ]

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"VEHICLE~{data.get('VIN')}"
            return data
        return data

    @classmethod
    async def find_by_vin(cls, vin: str) -> Optional["Vehicle"]:
        """Find a vehicle by VIN."""
        return await cls.find_one(cls.VIN == vin)

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

    def add_attachment(self, attachment: File):
        self.attachments.append(attachment)

    def add_expense(self, expense: Expense):
        if expense.VIN != self.VIN:
            raise ValueError("Expense VIN does not match vehicle VIN")
        if not expense.VIN:
            expense.VIN = self.VIN
        self.expenses.append(expense)

    def calculate_TCO(self) -> float:
        tco = (
            self.purchase_price
            + sum(expense.cost for expense in self.expenses)
            + sum(service.cost for service in self.service_records)
            + sum(fuel.cost for fuel in self.fuel_records)
        )
        return tco
