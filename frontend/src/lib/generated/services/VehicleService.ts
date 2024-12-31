/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OdometerReading } from '../models/OdometerReading';
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
}
