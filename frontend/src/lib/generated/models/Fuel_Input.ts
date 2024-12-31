/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { File } from './File';
import type { FuelType } from './FuelType';
/**
 * Fuel purchase record
 *
 * Attributes:
 * VIN (str): Vehicle Identification Number
 * date (DateTime): Date and time of fuel purchase
 * vendor_id (str): Fuel vendor ID
 * fuel_type (FuelType): Type of fuel purchased
 * units (float): Amount of fuel purchased
 * price_per_unit (float): Cost per unit of fuel
 * total_cost (float): Total cost of the fuel purchase
 */
export type Fuel_Input = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Vehicle VIN
     */
    VIN: string;
    date?: string;
    /**
     * Fuel vendor ID
     */
    vendor_id: string;
    /**
     * Type of fuel purchased
     */
    fuel_type: FuelType;
    /**
     * Units of fuel purchased
     */
    units: number;
    /**
     * Price per unit of fuel
     */
    price_per_unit: number;
    /**
     * Total cost of the fuel purchase
     */
    cost?: (number | null);
    /**
     * Documentation for the fuel purchase
     */
    attachments?: Array<File>;
};
