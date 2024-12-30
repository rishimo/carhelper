from enum import Enum

from models import File, User, Vehicle, Vendor


class EntityTypeToString(Enum):
    """
    Entity type enum
    """

    VEHICLE = "VEHICLE"
    VENDOR = "VENDOR"
    FILE = "FILE"
    USER = "USER"


class EntityTypeToClass(Enum):
    """
    Entity type to class mapping
    """

    VEHICLE = Vehicle
    VENDOR = Vendor
    FILE = File
    USER = User
