/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserPrivateView } from '../models/UserPrivateView';
import type { UserSignupInput } from '../models/UserSignupInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RegisterService {
    /**
     * User Registration
     * Create a new user.
     * @returns UserPrivateView Successful Response
     * @throws ApiError
     */
    public static userRegistrationRegisterPost({
        requestBody,
    }: {
        requestBody: UserSignupInput,
    }): CancelablePromise<UserPrivateView> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
