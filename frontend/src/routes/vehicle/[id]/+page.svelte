<script lang="ts">
	import { api } from '@lib/api';
	import { onMount } from 'svelte';
	import { toasts } from '@stores/toast';
	import type { Vehicle_Output } from '@lib/generated';
	import type {
		Service_Output,
		Fuel_Output,
		OdometerReading,
		Expense_Output
	} from '@lib/generated';
	import AddOdometerModal from '@components/AddOdometerModal.svelte';
	import AddServiceModal from '@components/AddServiceModal.svelte';
	import AddFuelModal from '@components/AddFuelModal.svelte';
	import UploadFileModal from '@components/UploadFileModal.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { theme } from '@lib/theme/colors';
	import { auth } from '@stores/auth';

	let vehicle: Vehicle_Output | null = null;
	let loading = true;
	let error = '';
	let vehicleLoaded = false;

	let showOdometerModal = false;
	let showServiceModal = false;
	let showFuelModal = false;
	let showFileModal = false;

	const vehicleId = $page.params.id;
	console.log('Page initialized with vehicleId:', vehicleId);

	// Subscribe to auth changes and load vehicle only once when auth is ready
	$: if (!$auth.loading) {
		console.log('Auth state ready, user:', $auth.user ? 'logged in' : 'not logged in');
		if ($auth.user && !vehicleLoaded) {
			console.log('Loading vehicle for the first time');
			vehicleLoaded = true;
			loadVehicle();
		} else if (!$auth.user) {
			console.log('User not logged in, redirecting to home');
			goto('/');
		}
	}

	async function loadVehicle() {
		try {
			console.log('Loading vehicle:', vehicleId);
			const response = await api.vehicle.getVehicleVehicleVehicleIdGet({
				vehicleId
			});
			console.log('Vehicle loaded:', response);
			vehicle = response;
		} catch (err) {
			console.error('Failed to load vehicle:', err);
			error = 'Failed to load vehicle details';
			toasts.error('Failed to load vehicle details');
			goto('/garage');
		} finally {
			loading = false;
		}
	}

	async function handleDelete() {
		try {
			console.log('Deleting vehicle:', vehicleId);
			if (!confirm('Are you sure you want to delete this vehicle?')) {
				console.log('Delete cancelled by user');
				return;
			}

			console.log('Sending delete request for vehicle ID:', vehicleId);
			await api.vehicle.deleteVehicleVehicleVehicleIdDelete({
				vehicleId
			});
			console.log('Vehicle deleted successfully');
			toasts.success('Vehicle deleted successfully');
			goto('/garage');
		} catch (err) {
			console.error('Failed to delete vehicle:', err);
			toasts.error('Failed to delete vehicle');
		}
	}

	function handleClick() {
		console.log('Simple click handler called');
		alert('Delete button clicked');
	}

	function formatDate(date: string) {
		return new Date(date).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function getTimelineEvents() {
		if (!vehicle) return [];

		const events: Array<{
			title: string;
			description?: string;
			date: string;
			type: 'odometer' | 'service' | 'fuel' | 'expense';
		}> = [];

		// Add odometer readings
		vehicle.odometer_records?.forEach((record: OdometerReading) => {
			if (record.date) {
				events.push({
					title: `Odometer Reading: ${record.reading.toLocaleString()} miles`,
					date: record.date,
					type: 'odometer'
				});
			}
		});

		// Add service records
		vehicle.service_records?.forEach((record: Service_Output) => {
			if (record.date) {
				const itemDescriptions = record.items.map((item) => item.description).join(', ');
				events.push({
					title: `Service: $${record.cost?.toFixed(2) || '0.00'}`,
					description: itemDescriptions || undefined,
					date: record.date,
					type: 'service'
				});
			}
		});

		// Add fuel records
		vehicle.fuel_records?.forEach((record: Fuel_Output) => {
			if (record.date) {
				const totalCost = record.cost ?? record.units * record.price_per_unit;
				events.push({
					title: `Fuel: ${record.units.toFixed(2)} gal @ $${record.price_per_unit.toFixed(2)}/gal`,
					description: `Total: $${totalCost.toFixed(2)}`,
					date: record.date,
					type: 'fuel'
				});
			}
		});

		// Add expenses
		vehicle.expenses?.forEach((record: Expense_Output) => {
			if (record.date) {
				events.push({
					title: record.description,
					description: `Amount: $${record.cost.toFixed(2)}`,
					date: record.date,
					type: 'expense'
				});
			}
		});

		// Sort by date, most recent first
		return events.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
	}
</script>

<div class="container mx-auto px-4 py-8">
	{#if loading}
		<div class="flex justify-center items-center h-64">
			<div
				class="animate-spin rounded-full h-12 w-12 border-t-2"
				style="border-color: {theme.primary}"
			/>
		</div>
	{:else if error}
		<div class="text-center text-red-500">{error}</div>
	{:else if vehicle}
		<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
			<!-- Vehicle Info -->
			<div class="col-span-1 space-y-6">
				<div class="bg-white rounded-lg shadow p-6">
					<h2 class="text-2xl font-bold mb-4" style="color: {theme.text}">
						{vehicle.make}
						{vehicle.model}
					</h2>
					<div class="space-y-2" style="color: {theme.textSecondary}">
						<p><span class="font-semibold">Year:</span> {vehicle.year}</p>
						<p><span class="font-semibold">VIN:</span> {vehicle.VIN}</p>
						{#if vehicle.color}
							<p><span class="font-semibold">Color:</span> {vehicle.color}</p>
						{/if}
						{#if vehicle.purchase_date}
							<p>
								<span class="font-semibold">Purchase Date:</span>
								{formatDate(vehicle.purchase_date)}
							</p>
						{/if}
						{#if vehicle.purchase_price}
							<p>
								<span class="font-semibold">Purchase Price:</span>
								${vehicle.purchase_price.toLocaleString()}
							</p>
						{/if}
					</div>
				</div>

				<!-- Quick Actions -->
				<div class="bg-white rounded-lg shadow p-6">
					<h3 class="text-lg font-semibold mb-4" style="color: {theme.text}">Quick Actions</h3>
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
						<hr class="border-t border-gray-200" />
						<button
							type="button"
							class="w-full px-4 py-2 text-white font-medium rounded-lg bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
							on:click={handleDelete}
						>
							Delete Vehicle
						</button>
					</div>
				</div>
			</div>

			<!-- Timeline -->
			<div class="col-span-1 md:col-span-2">
				<div class="bg-white rounded-lg shadow p-6">
					<h3 class="text-lg font-semibold mb-6" style="color: {theme.text}">Timeline</h3>
					{#if getTimelineEvents().length === 0}
						<p style="color: {theme.textSecondary}" class="text-center py-8">
							No events recorded yet
						</p>
					{:else}
						<div class="space-y-6">
							{#each getTimelineEvents() as event}
								<div class="flex items-start space-x-4">
									<div class="flex-shrink-0">
										<div
											class="h-4 w-4 rounded-full mt-2"
											style="background-color: {theme.primary}"
										/>
									</div>
									<div class="flex-grow">
										<div class="flex justify-between items-start">
											<h4 class="font-medium" style="color: {theme.text}">{event.title}</h4>
											<span style="color: {theme.textSecondary}">
												{formatDate(event.date)}
											</span>
										</div>
										{#if event.description}
											<p style="color: {theme.textSecondary}" class="mt-1">
												{event.description}
											</p>
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
		<AddOdometerModal bind:open={showOdometerModal} {vehicleId} onAdd={loadVehicle} />
		<AddServiceModal bind:open={showServiceModal} {vehicleId} onAdd={loadVehicle} />
		<AddFuelModal bind:open={showFuelModal} {vehicleId} onAdd={loadVehicle} />
		<UploadFileModal bind:open={showFileModal} {vehicleId} onUpload={loadVehicle} />
	{:else}
		<div style="color: {theme.textSecondary}" class="text-center">Vehicle not found</div>
	{/if}
</div>
