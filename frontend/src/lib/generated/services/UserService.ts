/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Expense_Input } from '../models/Expense_Input';
import type { UserPrivateView } from '../models/UserPrivateView';
import type { UserPublicView } from '../models/UserPublicView';
import type { UserUpdateInput } from '../models/UserUpdateInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UserService {
    /**
     * Get User
     * Return the requested user - public or private view.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUserUserGet({
        userId,
    }: {
        userId: string,
    }): CancelablePromise<(UserPublicView | UserPrivateView)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user',
            query: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update User
     * Update the user with the given input.
     * @returns UserPrivateView Successful Response
     * @throws ApiError
     */
    public static updateUserUserPatch({
        requestBody,
    }: {
        requestBody: UserUpdateInput,
    }): CancelablePromise<UserPrivateView> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/user',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Vehicles
     * Return the user's vehicles.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getVehiclesUserVehiclesGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user/vehicles',
        });
    }
    /**
     * Add Vehicle
     * Add a vehicle to the user's vehicles.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addVehicleUserVehiclesPost({
        vehicleId,
    }: {
        vehicleId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user/vehicles',
            query: {
                'vehicle_id': vehicleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Remove Vehicle
     * Remove a vehicle from the user's vehicles.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static removeVehicleUserVehiclesDelete({
        vehicleId,
    }: {
        vehicleId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/user/vehicles',
            query: {
                'vehicle_id': vehicleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Expenses
     * Return the user's expenses.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getExpensesUserExpensesGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user/expenses',
        });
    }
    /**
     * Add Expense
     * Add an expense to the user's expenses.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addExpenseUserExpensesPost({
        requestBody,
    }: {
        requestBody: Expense_Input,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user/expenses',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Remove Expense
     * Remove an expense from the user's expenses.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static removeExpenseUserExpensesDelete({
        expenseId,
    }: {
        expenseId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/user/expenses',
            query: {
                'expense_id': expenseId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
