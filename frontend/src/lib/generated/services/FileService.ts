/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FileReturn } from '../models/FileReturn';
import type { FileUpload } from '../models/FileUpload';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class FileService {
    /**
     * Upload File
     * Upload a file.
     * @returns string Successful Response
     * @throws ApiError
     */
    public static uploadFileFilePost({
        requestBody,
    }: {
        requestBody: FileUpload,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/file',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get File
     * Get a file by its ID.
     * Only the authorized user has access to the internal filename,
     * so we can use it to check if the user is the owner of the file.
     * @returns FileReturn Successful Response
     * @throws ApiError
     */
    public static getFileFileFileIdGet({
        fileId,
    }: {
        fileId: string,
    }): CancelablePromise<FileReturn> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/file/{file_id}',
            path: {
                'file_id': fileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete File
     * Delete a file.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteFileFileFileIdDelete({
        fileId,
    }: {
        fileId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/file/{file_id}',
            path: {
                'file_id': fileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
