from fastapi import APIRouter, Depends, HTTPException

from models import (Expense, User, UserPrivateView, UserPublicView,
                    UserUpdateInput)
from server.utils import current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=UserPublicView | UserPrivateView)
async def get_user(user_id: str, current: User | None = Depends(current_user)):
    """Return the requested user - public or private view."""
    # If user_id is 'me', use the current user
    if user_id == "me":
        if not current:
            raise HTTPException(401, "Not authenticated")
        return current.to_private_view()

    # Otherwise, look up the requested user
    user = await User.find_by_id(user_id)
    if user is None:
        raise HTTPException(404, "User not found")

    # If the requested user is the current user, return private view
    if current and user.id == current.id:
        return user.to_private_view()

    # Otherwise, return public view
    return user.to_public_view()


@router.patch("", response_model=UserPrivateView)
async def update_user(input: UserUpdateInput, user: User = Depends(current_user)):
    """Update the user with the given input."""
    await user.update_instance(input)
    return user.to_private_view()


@router.get("/vehicles")
async def get_vehicles(user: User = Depends(current_user)):
    """Return the user's vehicles."""
    return user.vehicle_ids


@router.post("/vehicles")
async def add_vehicle(vehicle_id: str, user: User = Depends(current_user)):
    """Add a vehicle to the user's vehicles."""
    await user.add_vehicle(vehicle_id)
    return user.vehicle_ids


@router.delete("/vehicles")
async def remove_vehicle(vehicle_id: str, user: User = Depends(current_user)):
    """Remove a vehicle from the user's vehicles."""
    await user.remove_vehicle(vehicle_id)
    return user.vehicle_ids


@router.get("/expenses")
async def get_expenses(user: User = Depends(current_user)):
    """Return the user's expenses."""
    return user.expenses


@router.post("/expenses")
async def add_expense(expense: Expense, user: User = Depends(current_user)):
    """Add an expense to the user's expenses."""
    await user.add_expense(expense)
    return user.expenses


@router.delete("/expenses")
async def remove_expense(expense_id: str, user: User = Depends(current_user)):
    """Remove an expense from the user's expenses."""
    await user.remove_expense(expense_id)
    return user.expenses
