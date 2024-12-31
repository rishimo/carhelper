/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_upload_file_vehicle__vehicle_id__files_post } from '../models/Body_upload_file_vehicle__vehicle_id__files_post';
import type { Fuel_Input } from '../models/Fuel_Input';
import type { Fuel_Output } from '../models/Fuel_Output';
import type { OdometerReading } from '../models/OdometerReading';
import type { Service_Input } from '../models/Service_Input';
import type { Service_Output } from '../models/Service_Output';
import type { Vehicle_Input } from '../models/Vehicle_Input';
import type { Vehicle_Output } from '../models/Vehicle_Output';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class VehicleService {
    /**
     * Create Vehicle
     * Create a new vehicle and associate it with the user.
     * @returns Vehicle_Output Successful Response
     * @throws ApiError
     */
    public static createVehicleVehiclePost({
        requestBody,
    }: {
        requestBody: Vehicle_Input,
    }): CancelablePromise<Vehicle_Output> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/vehicle',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get My Vehicles
     * Get all vehicles belonging to the current user.
     * @returns Vehicle_Output Successful Response
     * @throws ApiError
     */
    public static getMyVehiclesVehicleMyGet(): CancelablePromise<Array<Vehicle_Output>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/vehicle/my',
        });
    }
    /**
     * Get Vehicle
     * Get a specific vehicle by ID.
     * @returns Vehicle_Output Successful Response
     * @throws ApiError
     */
    public static getVehicleVehicleVehicleIdGet({
        vehicleId,
    }: {
        vehicleId: string,
    }): CancelablePromise<Vehicle_Output> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/vehicle/{vehicle_id}',
            path: {
                'vehicle_id': vehicleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Vehicle
     * Update a vehicle's details.
     * @returns Vehicle_Output Successful Response
     * @throws ApiError
     */
    public static updateVehicleVehicleVehicleIdPatch({
        vehicleId,
        requestBody,
    }: {
        vehicleId: string,
        requestBody: Record<string, any>,
    }): CancelablePromise<Vehicle_Output> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/vehicle/{vehicle_id}',
            path: {
                'vehicle_id': vehicleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Vehicle
     * Delete a vehicle and remove it from user's vehicles.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteVehicleVehicleVehicleIdDelete({
        vehicleId,
    }: {
        vehicleId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/vehicle/{vehicle_id}',
            path: {
                'vehicle_id': vehicleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Vehicle Stats
     * Get comprehensive stats for a vehicle.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getVehicleStatsVehicleVehicleIdStatsGet({
        vehicleId,
    }: {
        vehicleId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/vehicle/{vehicle_id}/stats',
            path: {
                'vehicle_id': vehicleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Odometer Reading
     * Add a new odometer reading for a vehicle.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addOdometerReadingVehicleVehicleIdOdometerPost({
        vehicleId,
        requestBody,
    }: {
        vehicleId: string,
        requestBody: OdometerReading,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/vehicle/{vehicle_id}/odometer',
            path: {
                'vehicle_id': vehicleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Service Record
     * Add a service record to a vehicle.
     * @returns Service_Output Successful Response
     * @throws ApiError
     */
    public static addServiceRecordVehicleVehicleIdServicePost({
        vehicleId,
        requestBody,
    }: {
        vehicleId: string,
        requestBody: Service_Input,
    }): CancelablePromise<Service_Output> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/vehicle/{vehicle_id}/service',
            path: {
                'vehicle_id': vehicleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Fuel Record
     * Add a fuel record to a vehicle.
     * @returns Fuel_Output Successful Response
     * @throws ApiError
     */
    public static addFuelRecordVehicleVehicleIdFuelPost({
        vehicleId,
        requestBody,
    }: {
        vehicleId: string,
        requestBody: Fuel_Input,
    }): CancelablePromise<Fuel_Output> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/vehicle/{vehicle_id}/fuel',
            path: {
                'vehicle_id': vehicleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Upload File
     * Upload a file associated with the vehicle.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static uploadFileVehicleVehicleIdFilesPost({
        vehicleId,
        formData,
        description,
    }: {
        vehicleId: string,
        formData: Body_upload_file_vehicle__vehicle_id__files_post,
        description?: (string | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/vehicle/{vehicle_id}/files',
            path: {
                'vehicle_id': vehicleId,
            },
            query: {
                'description': description,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
