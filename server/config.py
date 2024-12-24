from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    """Server config settings."""

    root_url: str = config("ROOT_URL", default="http://localhost:8080")

    # Mongo Engine settings
    mongodb_connection_string: str = config("MONGODB_CONNECTION_STRING")
    database_name: str = config("MONGODB_DATABASE_NAME")

    # Security settings
    authjwt_secret_key: str = config("SECRET_KEY")
    salt: bytes = config("SALT").encode()


CONFIG = Settings()
