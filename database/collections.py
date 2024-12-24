from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import IndexModel


COLLECTIONS: dict[str, dict[str, list[IndexModel]]] = {
    "users": {
        "indexes": [
            IndexModel([("email", 1)], unique=True),
        ]
    },
    "vendors": {
        "indexes": [
            IndexModel([("name", 1)]),
            IndexModel([("location.city", 1), ("location.state", 1)]),
        ]
    },
    "vehicles": {
        "indexes": [
            IndexModel([("user_id", 1)]),
            IndexModel([("VIN", 1)], unique=True),
            IndexModel([("service_records.date", -1)]),
            IndexModel([("fuel_records.date", -1)]),
            IndexModel([("odometer_records.date", -1)]),
        ]
    },
}
