from fastapi import APIRouter, HTTPException, Response, Security
from fastapi_jwt import JwtAuthorizationCredentials

from models import User, UserAuthInput
from models.auth import AccessToken, RefreshToken
from server.jwt import access_security, refresh_security
from server.utils import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(input: UserAuthInput, response: Response) -> AccessToken:
    """Authenticate and returns the user's JWT."""
    user = await User.find_by_email(input.email)
    if user is None or hash_password(input.password) != user.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    access_token = access_security.create_access_token(user.jwt_subject)
    refresh_token = refresh_security.create_refresh_token(user.jwt_subject)

    # Set refresh token as secure HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,  # 30 days
    )

    return AccessToken(access_token=access_token)


@router.post("/refresh")
async def refresh(
    auth: JwtAuthorizationCredentials = Security(refresh_security),
) -> AccessToken:
    """Return a new access token from a refresh token."""
    access_token = access_security.create_access_token(subject=auth.subject)
    return AccessToken(access_token=access_token)
