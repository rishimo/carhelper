from enum import Enum


class FileType(str, Enum):
    """
    File type enum
    """

    REPAIR_MANUAL = "REPAIR_MANUAL"
    SERVICE_RECORD = "SERVICE_RECORD"
    RECEIPT = "RECEIPT"
    INVOICE = "INVOICE"
    OWNER_MANUAL = "OWNER_MANUAL"
    SERVICE_INTERVAL = "SERVICE_INTERVAL"
    WARRANTY = "WARRANTY"


class ExpenseType(str, Enum):
    """
    Expense type enum
    """

    PARTS = "PARTS"
    MODS = "MODS"
    TOOLS = "TOOLS"
    OTHER = "OTHER"


class ServiceType(str, Enum):
    """
    Service type enum
    """

    MAINTENANCE = "MAINTENANCE"
    REPAIR = "REPAIR"
    MODIFICATION = "MODIFICATION"
    INSPECTION = "INSPECTION"


class FuelType(str, Enum):
    """
    Fuel type enum
    """

    REGULAR = "Regular"
    PREMIUM = "Premium"
    DIESEL = "Diesel"
    ELECTRICITY = "Electricity"
    OTHER = "Other"
