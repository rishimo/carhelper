/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Location model
 */
export type Location = {
    address: string;
    city: string;
    state: string;
    zip_code: string;
    /**
     * Latitude of the location
     */
    latitude?: (number | null);
    /**
     * Longitude of the location
     */
    longitude?: (number | null);
};
