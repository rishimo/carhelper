import { api } from '@/lib/api';
import type { Vehicle_Input, OdometerReading, Service_Input, Fuel_Input } from '@/lib/generated';
import type { Body_upload_file_vehicle__vehicle_id__files_post } from '@/lib/generated/models/Body_upload_file_vehicle__vehicle_id__files_post';

export const vehicleService = {
	// Vehicle CRUD operations
	getAll: () => api.vehicle.getMyVehiclesVehicleMyGet(),
	get: (id: string) => api.vehicle.getVehicleVehicleVehicleIdGet({ vehicleId: id }),
	create: (data: Vehicle_Input) => api.vehicle.createVehicleVehiclePost({ requestBody: data }),
	update: (id: string, data: Partial<Vehicle_Input>) =>
		api.vehicle.updateVehicleVehicleVehicleIdPatch({ vehicleId: id, requestBody: data }),
	delete: (id: string) => api.vehicle.deleteVehicleVehicleVehicleIdDelete({ vehicleId: id }),

	// Vehicle stats
	getStats: (id: string) => api.vehicle.getVehicleStatsVehicleVehicleIdStatsGet({ vehicleId: id }),

	// Records management
	addOdometerReading: (id: string, data: OdometerReading) =>
		api.vehicle.addOdometerReadingVehicleVehicleIdOdometerPost({
			vehicleId: id,
			requestBody: data
		}),
	addServiceRecord: (id: string, data: Service_Input) =>
		api.vehicle.addServiceRecordVehicleVehicleIdServicePost({ vehicleId: id, requestBody: data }),
	addFuelRecord: (id: string, data: Fuel_Input) =>
		api.vehicle.addFuelRecordVehicleVehicleIdFuelPost({ vehicleId: id, requestBody: data }),
	uploadFile: (id: string, file: File, description?: string) => {
		const formData: Body_upload_file_vehicle__vehicle_id__files_post = { file };
		return api.vehicle.uploadFileVehicleVehicleIdFilesPost({
			vehicleId: id,
			formData,
			description
		});
	}
};
