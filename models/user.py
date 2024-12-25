from typing import Dict, List, Optional

from pendulum import now, today
from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime
from pymongo.operations import IndexModel

from models.base import CustomIDModel
from models.expense import Expense
from models.utils import create_hash


class UserAuthInput(BaseModel):
    """User authentication input model."""

    email: EmailStr
    password: str


class UserSignupInput(UserAuthInput):
    """User signup input model."""

    username: str
    first_name: str
    last_name: str


class UserPublicView(BaseModel):
    """Public user information visible to other users."""

    username: str
    bio: Optional[str] = ""
    join_date: DateTime


class UserPrivateView(UserPublicView):
    """Private user information only visible to the user themselves."""

    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    vehicle_ids: List[str] = Field(default_factory=list)
    expenses: List[Expense] = Field(default_factory=list)
    last_login: DateTime


class UserUpdateInput(BaseModel):
    """User update input model."""

    email: Optional[EmailStr] = Field(default=None)
    username: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)


class User(CustomIDModel):
    """Complete User model for database storage."""

    email: EmailStr = Field(description="User email")
    password: str = Field(description="User password")
    username: str = Field(description="User username")
    bio: Optional[str] = Field(description="User bio", default="")
    first_name: str = Field(description="User first name")
    last_name: str = Field(description="User last name")
    phone_number: Optional[str] = Field(description="User phone number", default="")
    vehicle_ids: List[str] = Field(
        description="User vehicles, list of VINs", default_factory=list
    )
    expenses: List[Expense] = Field(
        description="User's expenses (not associated with a vehicle)",
        default_factory=list,
    )
    join_date: DateTime = Field(description="User join date", default=now())
    last_login: DateTime = Field(description="User last login date", default=now())

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", 1)], unique=True),
            IndexModel([("username", 1)], unique=True),
            IndexModel([("join_date", -1), ("last_login", -1)]),
            IndexModel([("vehicle_ids", 1)]),
        ]

    def to_public_view(self) -> UserPublicView:
        """Convert to public view model."""
        return UserPublicView(
            username=self.username, bio=self.bio, join_date=self.join_date
        )

    def to_private_view(self) -> UserPrivateView:
        """Convert to private view model."""
        return UserPrivateView(
            username=self.username,
            bio=self.bio,
            join_date=self.join_date,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            vehicle_ids=self.vehicle_ids,
            expenses=self.expenses,
            last_login=self.last_login,
        )

    @classmethod
    def from_signup(cls, input_data: UserSignupInput, **additional_fields) -> "User":
        """Create a new user from signup data."""
        return cls(
            email=input_data.email,
            password=input_data.password,
            username=input_data.username,
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            **additional_fields,
        )

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = f"USER~{create_hash(data.get('email'))}"
            return data
        return data

    @classmethod
    async def find_by_email(cls, email: EmailStr) -> Optional["User"]:
        """Find a user by email."""
        return await cls.find_one(cls.email == email)

    @classmethod
    async def find_by_username(cls, username: str) -> Optional["User"]:
        """Find a user by username."""
        return await cls.find_one(cls.username == username)

    async def add_vehicle(self, vehicle_id: str):
        self.vehicle_ids.append(vehicle_id)
        await self.save()
        return True

    async def remove_vehicle(self, vehicle_id: str) -> bool:
        self.vehicle_ids.remove(vehicle_id)
        await self.save()
        return True

    async def add_expense(self, expense: Expense) -> bool:
        self.expenses.append(expense)
        await self.save()
        return True

    async def remove_expense(self, expense_id: str) -> bool:
        self.expenses.remove(expense_id)
        await self.save()
        return True

    @property
    def jwt_subject(self) -> Dict[str, str]:
        return {"id": self.id, "email": self.email}
