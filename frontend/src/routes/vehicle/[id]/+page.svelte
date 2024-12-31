<script lang="ts">
	import { api } from '@/lib/api';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import type { Vehicle_Output } from '@models/Vehicle_Output';
	import type { TimelineEvent } from '@models/TimelineEvent';
	import AddOdometerModal from '@components/AddOdometerModal.svelte';
	import AddServiceModal from '@components/AddServiceModal.svelte';
	import AddFuelModal from '@components/AddFuelModal.svelte';
	import UploadFileModal from '@components/UploadFileModal.svelte';
	import { page } from '$app/stores';

	let vehicle: Vehicle_Output | null = null;
	let timeline: Array<TimelineEvent> = [];
	let loading = true;
	let error = '';

	let showOdometerModal = false;
	let showServiceModal = false;
	let showFuelModal = false;
	let showFileModal = false;

	const vehicleId = $page.params.id;

	async function loadVehicle() {
		try {
			vehicle = await api.vehicle.getVehicleVehicleVehicleIdGet({ vehicleId });
		} catch (err) {
			console.error('Failed to load vehicle:', err);
			error = 'Failed to load vehicle details';
		}
	}

	async function loadTimeline() {
		try {
			timeline = await api.vehicle.getTimelineVehicleVehicleIdTimelineGet({ vehicleId });
		} catch (err) {
			console.error('Failed to load timeline:', err);
			error = 'Failed to load timeline';
		}
	}

	async function refreshData() {
		loading = true;
		error = '';
		await Promise.all([loadVehicle(), loadTimeline()]);
		loading = false;
	}

	onMount(refreshData);

	function formatDate(date: string) {
		return new Date(date).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}
</script>

<div class="container mx-auto px-4 py-8">
	{#if loading}
		<div class="flex justify-center items-center h-64">
			<div class="animate-spin rounded-full h-12 w-12 border-t-2 border-primary" />
		</div>
	{:else if error}
		<div class="text-center text-red-500">{error}</div>
	{:else if vehicle}
		<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
			<!-- Vehicle Info -->
			<div class="col-span-1 space-y-6">
				<div class="bg-white rounded-lg shadow p-6">
					<h2 class="text-2xl font-bold mb-4">{vehicle.make} {vehicle.model}</h2>
					<div class="space-y-2">
						<p><span class="font-semibold">Year:</span> {vehicle.year}</p>
						<p><span class="font-semibold">VIN:</span> {vehicle.VIN}</p>
						<p><span class="font-semibold">License Plate:</span> {vehicle.license_plate}</p>
					</div>
				</div>

				<!-- Quick Actions -->
				<div class="bg-white rounded-lg shadow p-6">
					<h3 class="text-lg font-semibold mb-4">Quick Actions</h3>
					<div class="space-y-3">
						<button class="btn btn-primary w-full" on:click={() => (showOdometerModal = true)}>
							Add Odometer Reading
						</button>
						<button class="btn btn-primary w-full" on:click={() => (showServiceModal = true)}>
							Add Service Record
						</button>
						<button class="btn btn-primary w-full" on:click={() => (showFuelModal = true)}>
							Add Fuel Record
						</button>
						<button class="btn btn-primary w-full" on:click={() => (showFileModal = true)}>
							Upload File
						</button>
					</div>
				</div>
			</div>

			<!-- Timeline -->
			<div class="col-span-1 md:col-span-2">
				<div class="bg-white rounded-lg shadow p-6">
					<h3 class="text-lg font-semibold mb-6">Timeline</h3>
					{#if timeline.length === 0}
						<p class="text-gray-500 text-center py-8">No events recorded yet</p>
					{:else}
						<div class="space-y-6">
							{#each timeline as event}
								<div class="flex items-start space-x-4">
									<div class="flex-shrink-0">
										<div class="h-4 w-4 rounded-full bg-primary mt-2" />
									</div>
									<div class="flex-grow">
										<div class="flex justify-between items-start">
											<h4 class="font-medium">{event.title}</h4>
											<span class="text-sm text-gray-500">{formatDate(event.date)}</span>
										</div>
										{#if event.description}
											<p class="text-gray-600 mt-1">{event.description}</p>
										{/if}
									</div>
								</div>
							{/each}
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- Modals -->
		<AddOdometerModal bind:open={showOdometerModal} {vehicleId} onAdd={refreshData} />
		<AddServiceModal bind:open={showServiceModal} {vehicleId} onAdd={refreshData} />
		<AddFuelModal bind:open={showFuelModal} {vehicleId} onAdd={refreshData} />
		<UploadFileModal bind:open={showFileModal} {vehicleId} onUpload={refreshData} />
	{:else}
		<div class="text-center text-gray-500">Vehicle not found</div>
	{/if}
</div>
