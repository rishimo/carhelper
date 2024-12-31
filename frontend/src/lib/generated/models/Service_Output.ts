/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ServiceItem_Output } from './ServiceItem_Output';
/**
 * Complete service record for a vehicle service visit
 *
 * Attributes:
 * VIN (str): Vehicle Identification Number
 * date (DateTime): Date and time of the service
 * vendor_id (str): Service provider ID
 * total_cost (float): Total cost of all service items
 * items (List[ServiceItem]): List of individual service items performed
 */
export type Service_Output = {
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
     * Service vendor ID
     */
    vendor_id: string;
    /**
     * Total cost of all service items
     */
    cost?: (number | null);
    items: Array<ServiceItem_Output>;
};
