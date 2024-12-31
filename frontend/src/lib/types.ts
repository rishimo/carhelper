export interface User {
	id: string;
	email: string;
	username: string;
	bio?: string;
	first_name: string;
	last_name: string;
	phone_number?: string;
	vehicle_ids: Array<string>;
	expenses: Array<Expense>;
	join_date: string;
	last_login: string;
	file_ids: Array<string>;
}

export interface Vehicle {
	id: string;
	VIN: string;
	make: string;
	model: string;
	year: number;
	color?: string;
	owner_id?: string;
	purchase_date?: string;
	purchase_price?: number;
	odometer_records: Array<OdometerReading>;
	service_records: Array<Service>;
	fuel_records: Array<Fuel>;
	expenses: Array<Expense>;
	file_ids: Array<string>;
}

export interface VehicleStats {
	current_mileage: number;
	total_cost_of_ownership: number;
	recent_services: Array<Service>;
	fuel_efficiency?: number;
	total_service_records: number;
	total_fuel_records: number;
	total_expenses: number;
}

export interface OdometerReading {
	id: string;
	VIN: string;
	date: string;
	reading: number;
	location?: Location;
}

export interface Service {
	id: string;
	VIN: string;
	date: string;
	vendor_id: string;
	cost: number;
	items: Array<ServiceItem>;
}

export interface ServiceItem {
	id: string;
	service_type: string;
	description: string;
	cost: number;
	attachments: Array<File>;
}

export interface Fuel {
	id: string;
	VIN: string;
	date: string;
	vendor_id: string;
	fuel_type: string;
	units: number;
	price_per_unit: number;
	cost: number;
	attachments: Array<File>;
}

export interface Expense {
	id: string;
	VIN?: string;
	date: string;
	vendor: Vendor;
	description: string;
	cost: number;
	file_ids: Array<string>;
	items: Array<ExpenseItem>;
}

export interface ExpenseItem {
	id: string;
	expense_type: string;
	description: string;
	cost: number;
	file_ids: Array<string>;
}

export interface Vendor {
	id: string;
	name: string;
	website?: string;
	email?: string;
	phone_number?: string;
	location: Location;
}

export interface Location {
	address: string;
	city: string;
	state: string;
	zip_code: string;
}

export interface File {
	id: string;
	type: string;
	title: string;
	internal_filename: string;
	description?: string;
	owner_user_id: string;
	entity_id: string;
	page_content?: string;
}
