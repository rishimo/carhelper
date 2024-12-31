/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Expense_Output } from './Expense_Output';
/**
 * Private user information only visible to the user themselves.
 */
export type UserPrivateView = {
    username: string;
    bio?: (string | null);
    join_date: string;
    email: string;
    first_name: string;
    last_name: string;
    phone_number: (string | null);
    vehicle_ids?: Array<string>;
    expenses?: Array<Expense_Output>;
    last_login: string;
};
