/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Location } from './Location';
/**
 * Vehicle odometer reading record
 *
 * Attributes:
 * VIN (str): Vehicle Identification Number
 * date (DateTime): Date and time of the reading
 * reading (float): Odometer value
 * location (Optional[Location]): Location where reading was taken
 */
export type OdometerReading = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Vehicle VIN
     */
    VIN: string;
    date?: string;
    reading: number;
    /**
     * Odometer reading location
     */
    location?: (Location | null);
};

