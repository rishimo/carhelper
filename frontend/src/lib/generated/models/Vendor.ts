/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Location } from './Location';
/**
 * Vendor model representing service providers and suppliers
 *
 * Attributes:
 * name (str): Name of the vendor/business
 * website (Optional[HttpUrl]): Vendor's website URL
 * email (Optional[EmailStr]): Contact email address
 * phone_number (Optional[str]): Contact phone number
 * location (Location): Physical location of the vendor
 */
export type Vendor = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Vendor name
     */
    name: string;
    /**
     * Vendor website
     */
    website?: (string | null);
    /**
     * Vendor email
     */
    email?: (string | null);
    /**
     * Vendor phone number
     */
    phone_number?: (string | null);
    /**
     * Vendor location
     */
    location: Location;
};

