/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { File } from './File';
import type { ServiceType } from './ServiceType';
/**
 * Individual service item or task performed during a service visit
 *
 * Attributes:
 * service_type (ServiceType): Type of service performed (e.g., MAINTENANCE)
 * description (str): Detailed description of the service performed
 * cost (float): Cost of the individual service item
 * attachments (List[File]): Related documentation for the service item
 */
export type ServiceItem_Output = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Service type
     */
    service_type?: ServiceType;
    /**
     * Service description
     */
    description: string;
    /**
     * Service cost
     */
    cost: number;
    /**
     * Documentation for the service
     */
    attachments?: Array<File>;
};
