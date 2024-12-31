/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExpenseItem } from './ExpenseItem';
import type { Vendor } from './Vendor';
/**
 * Expense record, for any other expenses like parts, mods, tools, etc.
 */
export type Expense_Output = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Vehicle VIN
     */
    VIN?: (string | null);
    date?: string;
    /**
     * Expense vendor
     */
    vendor: Vendor;
    /**
     * Expense description
     */
    description: string;
    /**
     * Expense cost
     */
    cost: number;
    /**
     * File IDs for the expense
     */
    file_ids?: Array<string>;
    /**
     * Expense items
     */
    items?: Array<ExpenseItem>;
};
