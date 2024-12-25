from fastapi import APIRouter, HTTPException

from models import User, UserPrivateView, UserSignupInput
from server.utils import hash_password

router = APIRouter(prefix="/register", tags=["register"])


@router.post("", response_model=UserPrivateView)
async def user_registration(input: UserSignupInput):
    """Create a new user."""

    user = await User.find_by_email(input.email)
    if user is not None:
        raise HTTPException(409, "User with that email already exists")

    hashed = hash_password(input.password)
    input.password = hashed

    user = User.from_signup(input)
    await user.create()
    return user.to_private_view()
