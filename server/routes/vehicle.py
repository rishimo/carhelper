from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from models import File as VehicleFile
from models import Fuel, OdometerReading, Service, User, Vehicle
from server.utils import current_user

router = APIRouter(prefix="/vehicle", tags=["vehicle"])


@router.post("", response_model=Vehicle)
async def create_vehicle(vehicle: Vehicle, user: User = Depends(current_user)):
    """Create a new vehicle and associate it with the user."""
    # Check if vehicle already exists
    existing = await Vehicle.find_by_vin(vehicle.VIN)
    if existing is not None:
        raise HTTPException(409, "Vehicle with that VIN already exists")

    # Create vehicle
    await vehicle.create()

    # Associate with user
    await user.add_vehicle(vehicle.id)

    return vehicle


@router.get("/my", response_model=List[Vehicle])
async def get_my_vehicles(user: User = Depends(current_user)):
    """Get all vehicles belonging to the current user."""
    vehicles = []
    for vehicle_id in user.vehicle_ids:
        vehicle = await Vehicle.find_by_id(vehicle_id)
        if vehicle:
            vehicles.append(vehicle)
    return vehicles


@router.get("/{vehicle_id}", response_model=Vehicle)
async def get_vehicle(vehicle_id: str, user: User = Depends(current_user)):
    """Get a specific vehicle by ID."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    return vehicle


@router.patch("/{vehicle_id}", response_model=Vehicle)
async def update_vehicle(
    vehicle_id: str, update_data: dict, user: User = Depends(current_user)
):
    """Update a vehicle's details."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    await vehicle.update(update_data)
    return vehicle


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: str, user: User = Depends(current_user)):
    """Delete a vehicle and remove it from user's vehicles."""
    # First remove from user's vehicles
    await user.remove_vehicle(vehicle_id)

    # Then delete the vehicle itself
    vehicle = await Vehicle.find_by_id(vehicle_id)
    if vehicle:
        await vehicle.delete()

    return {"message": "Vehicle deleted successfully"}


@router.get("/{vehicle_id}/stats")
async def get_vehicle_stats(vehicle_id: str, user: User = Depends(current_user)):
    """Get comprehensive stats for a vehicle."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    try:
        current_mileage = vehicle.current_mileage()
    except ValueError:
        current_mileage = 0

    total_cost = vehicle.calculate_TCO()

    # Calculate service history
    service_history = sorted(
        vehicle.service_records, key=lambda x: x.date, reverse=True
    )
    recent_services = service_history[:5] if service_history else []

    # Calculate fuel efficiency if we have enough data
    fuel_efficiency = None
    if len(vehicle.fuel_records) > 1 and len(vehicle.odometer_records) > 1:
        total_fuel = sum(record.units for record in vehicle.fuel_records)
        mileage_diff = (
            vehicle.odometer_records[-1].reading - vehicle.odometer_records[0].reading
        )
        if total_fuel > 0:
            fuel_efficiency = mileage_diff / total_fuel

    return {
        "current_mileage": current_mileage,
        "total_cost_of_ownership": total_cost,
        "recent_services": recent_services,
        "fuel_efficiency": fuel_efficiency,
        "total_service_records": len(service_history),
        "total_fuel_records": len(vehicle.fuel_records),
        "total_expenses": len(vehicle.expenses),
    }


@router.post("/{vehicle_id}/odometer")
async def add_odometer_reading(
    vehicle_id: str, reading: OdometerReading, user: User = Depends(current_user)
):
    """Add a new odometer reading for a vehicle."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    vehicle.add_odometer_record(reading)
    await vehicle.save()

    return reading


@router.post("/{vehicle_id}/service", response_model=Service)
async def add_service_record(
    vehicle_id: str, record: Service, user: User = Depends(current_user)
):
    """Add a service record to a vehicle."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    await vehicle.add_service_record(record)
    return record


@router.post("/{vehicle_id}/fuel", response_model=Fuel)
async def add_fuel_record(
    vehicle_id: str, record: Fuel, user: User = Depends(current_user)
):
    """Add a fuel record to a vehicle."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    await vehicle.add_fuel_record(record)
    return record


@router.post("/{vehicle_id}/files")
async def upload_file(
    vehicle_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    user: User = Depends(current_user),
):
    """Upload a file associated with the vehicle."""
    if vehicle_id not in user.vehicle_ids:
        raise HTTPException(403, "You don't have access to this vehicle")

    vehicle = await Vehicle.find_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")

    # Read and store file
    contents = await file.read()
    vehicle_file = VehicleFile(
        filename=file.filename,
        content_type=file.content_type,
        description=description,
        data=contents,
    )

    await vehicle.add_file(vehicle_file)
    return vehicle_file
