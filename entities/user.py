from typing import List, Optional

from entities.base import CustomIDModel
from entities.expense import Expense
from entities.utils import create_hash

from pendulum import now, today
from pydantic import Field, model_validator, EmailStr
from pydantic_extra_types.pendulum_dt import DateTime
from pymongo.operations import IndexModel


class User(CustomIDModel):
    """
    User model

    Attributes:
        email (EmailStr): User email
        bio (Optional[str]): User bio
        display_name (str): User display name
        first_name (str): User first name
        last_name (str): User last name
        phone_number (Optional[str]): User phone number
        vehicle_ids (List[str]): User vehicles, list of VINs
        expenses (List[Expense]): User's expenses (not associated with a vehicle)
        join_date (DateTime): User join date
        last_login (DateTime): User last login date
    """

    email: EmailStr = Field(description="User email")
    bio: Optional[str] = Field(description="User bio", default="")
    display_name: str = Field(description="User display name")
    first_name: str = Field(description="User first name")
    last_name: str = Field(description="User last name")
    phone_number: Optional[str] = Field(description="User phone number")
    vehicle_ids: Optional[List[str]] = Field(
        description="User vehicles, list of VINs", default_factory=list
    )
    expenses: Optional[List[Expense]] = Field(
        description="User's expenses (not associated with a vehicle)",
        default_factory=list,
    )
    join_date: DateTime = Field(description="User join date", default=today())
    last_login: DateTime = Field(description="User last login date", default=now())

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", 1)], unique=True),
            IndexModel(
                [("display_name", 1)], unique=True
            ),  # TODO: support Atlas search
            IndexModel([("join_date", -1), ("last_login", -1)]),
            IndexModel([("vehicle_ids", 1)]),
        ]

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"USER~{create_hash(data.get('email'))}"
            return data
        return data

    def add_vehicle(self, vehicle_id: str):
        self.vehicle_ids.append(vehicle_id)

    def add_expense(self, expense: Expense):
        self.expenses.append(expense)
