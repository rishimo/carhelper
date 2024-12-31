/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExpenseType } from './ExpenseType';
/**
 * Expense item record, for any other expenses like parts, mods, tools, etc.
 */
export type ExpenseItem = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * Expense type
     */
    expense_type: ExpenseType;
    /**
     * Expense description
     */
    description: string;
    /**
     * Expense cost
     */
    cost: number;
    /**
     * File IDs for the expense item
     */
    file_ids?: Array<string>;
};
