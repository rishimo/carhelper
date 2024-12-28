from typing import Optional

import bcrypt
from fastapi import HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from pendulum import now
from slugify import slugify

from models import User
from models.enums import FileType
from server import CONFIG
from server.jwt import access_security, user_from_credentials


def hash_password(password: str) -> str:
    """Return a salted password hash."""
    return bcrypt.hashpw(password.encode(), CONFIG.salt).decode()


async def current_user(
    auth: Optional[JwtAuthorizationCredentials] = Security(access_security),
) -> User:
    """Return the current authorized user."""
    if not auth:
        raise HTTPException(401, "No authorization credentials found")
    user = await user_from_credentials(auth)
    if user is None:
        raise HTTPException(404, "Authorized user could not be found")
    return user


def construct_filename(upload_filename: str, file_type: FileType, user_id: str) -> str:
    """Construct a file name for storage."""

    # Clean up the filename
    filename = slugify(upload_filename)

    # Add the file type and timestamp to the filename
    return f"{user_id}/{file_type.value}/{filename}/{now().to_iso8601_string()}"
