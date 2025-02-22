import { AuthService } from '@services/AuthService';
import { RegisterService } from '@services/RegisterService';
import { UserService } from '@services/UserService';
import { VehicleService } from '@services/VehicleService';
import { OpenAPI } from '@core/OpenAPI';
import { browser } from '$app/environment';

// Configure base URL and credentials
OpenAPI.BASE = 'http://localhost:8000';
OpenAPI.WITH_CREDENTIALS = true;
OpenAPI.CREDENTIALS = 'include';

// Add auth token to requests
if (browser) {
	const token = localStorage.getItem('token');
	if (token) {
		OpenAPI.HEADERS = {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		};
	} else {
		OpenAPI.HEADERS = {
			'Content-Type': 'application/json'
		};
	}
}

export const api = {
	auth: AuthService,
	register: RegisterService,
	user: UserService,
	vehicle: VehicleService
};

export { OpenAPI };
