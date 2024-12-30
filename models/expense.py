from typing import List, Optional

from pendulum import today
from pydantic import Field, model_validator
from pydantic_extra_types.pendulum_dt import DateTime

from models.base import CustomIDModel
from models.enums import ExpenseType
from models.utils import create_hash
from models.vendor import Vendor


class ExpenseItem(CustomIDModel):
    """
    Expense item record, for any other expenses like parts, mods, tools, etc.
    """

    expense_type: ExpenseType = Field(description="Expense type")
    description: str = Field(description="Expense description")
    cost: float = Field(description="Expense cost")
    file_ids: List[str] = Field(
        description="File IDs for the expense item", default_factory=list
    )


class Expense(CustomIDModel):
    """
    Expense record, for any other expenses like parts, mods, tools, etc.
    """

    VIN: Optional[str] = Field(description="Vehicle VIN", default=None)
    date: DateTime = Field(default_factory=today)
    vendor: Vendor = Field(description="Expense vendor")
    description: str = Field(description="Expense description")
    cost: float = Field(description="Expense cost")
    file_ids: List[str] = Field(
        description="File IDs for the expense", default_factory=list
    )
    items: List[ExpenseItem] = Field(description="Expense items", default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def calculate_cost(cls, data: dict) -> dict:
        if data.get("cost") is None:
            data["cost"] = sum(item.cost for item in data.get("items", []))
        return data

    @model_validator(mode="before")
    @classmethod
    def generate_id(cls, data: dict) -> dict:
        if data.get("id") is None:
            data["id"] = (
                f"EXPENSE~{create_hash(data.get('VIN', ''), str(data.get('date', '')))}"
            )
        return data
