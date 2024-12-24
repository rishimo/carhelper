from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import Duration

from server.jwt import ACCESS_EXPIRES, REFRESH_EXPIRES


class AccessToken(BaseModel):
    """Access token model."""

    access_token: str
    access_token_expires: Duration = ACCESS_EXPIRES


class RefreshToken(BaseModel):
    """Refresh token model."""

    refresh_token: str
    refresh_token_expires: Duration = REFRESH_EXPIRES
