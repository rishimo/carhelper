from typing import Optional

from fastapi_jwt import (JwtAccessBearer, JwtAuthorizationCredentials,
                         JwtRefreshBearer)
from pendulum import duration

from models import User
from server import CONFIG

ACCESS_EXPIRES = duration(minutes=15)
REFRESH_EXPIRES = duration(days=30)

access_security = JwtAccessBearer(
    CONFIG.authjwt_secret_key,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)

refresh_security = JwtRefreshBearer(
    CONFIG.authjwt_secret_key,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)


async def user_from_credentials(auth: JwtAuthorizationCredentials) -> Optional[User]:
    """Return the user associated with auth credentials."""
    return await User.find_by_email(auth.subject["email"])


async def user_from_token(token: str) -> Optional[User]:
    """Return the user associated with a token value."""
    payload = access_security._decode(token)
    return await User.find_by_email(payload["subject"]["email"])
