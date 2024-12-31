/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessToken } from '../models/AccessToken';
import type { UserAuthInput } from '../models/UserAuthInput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthService {
	/**
	 * Login
	 * Authenticate and returns the user's JWT.
	 * @returns AccessToken Successful Response
	 * @throws ApiError
	 */
	public static loginAuthLoginPost({
		requestBody
	}: {
		requestBody: UserAuthInput;
	}): CancelablePromise<AccessToken> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/auth/login',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				422: `Validation Error`
			}
		});
	}
	/**
	 * Refresh
	 * Return a new access token from a refresh token.
	 * @returns AccessToken Successful Response
	 * @throws ApiError
	 */
	public static refreshAuthRefreshPost(): CancelablePromise<AccessToken> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/auth/refresh'
		});
	}
}
