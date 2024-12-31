/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Expense_Output } from './Expense_Output';
import type { Fuel_Output } from './Fuel_Output';
import type { OdometerReading } from './OdometerReading';
import type { Service_Output } from './Service_Output';
/**
 * Primary vehicle record containing all vehicle-related information
 *
 * Attributes:
 * VIN (str): Vehicle Identification Number
 * make (str): Vehicle manufacturer
 * model (str): Vehicle model name
 * year (int): Vehicle manufacturing year
 * color (Optional[str]): Vehicle color, defaults to "NOT_SET"
 * owner_id (Optional[str]): Vehicle owner ID
 * odometer_records (Optional[List[OdometerReading]]): History of odometer readings
 * service_records (Optional[List[Service]]): History of service visits
 * fuel_records (Optional[List[Fuel]]): History of fuel purchases
 * documentation (Optional[List[Documentation]]): Vehicle-related documentation
 */
export type Vehicle_Output = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Vehicle VIN
     */
    VIN: string;
    /**
     * Vehicle make
     */
    make: string;
    /**
     * Vehicle model
     */
    model: string;
    /**
     * Vehicle year
     */
    year: number;
    /**
     * Vehicle color
     */
    color?: (string | null);
    /**
     * Vehicle owner ID
     */
    owner_id?: (string | null);
    /**
     * Vehicle purchase date
     */
    purchase_date?: (string | null);
    /**
     * Vehicle purchase price
     */
    purchase_price?: (number | null);
    /**
     * Odometer records
     */
    odometer_records?: (Array<OdometerReading> | null);
    /**
     * Service records
     */
    service_records?: (Array<Service_Output> | null);
    /**
     * Fuel records
     */
    fuel_records?: (Array<Fuel_Output> | null);
    /**
     * Expenses
     */
    expenses?: (Array<Expense_Output> | null);
    /**
     * File IDs
     */
    file_ids?: (Array<string> | null);
};
