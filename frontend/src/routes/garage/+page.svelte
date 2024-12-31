<script lang="ts">
	import { api } from '@lib/api';
	import { onMount } from 'svelte';
	import { Plus } from 'lucide-svelte';
	import type { Vehicle_Output } from '@models/Vehicle_Output';
	import VehicleCard from '@components/VehicleCard.svelte';
	import AddVehicleModal from '@components/AddVehicleModal.svelte';
	import Modal from '@components/Modal.svelte';
	import { toast } from 'svelte-sonner';
	import { auth } from '@stores/auth';
	import { goto } from '$app/navigation';

	let vehicles: Array<Vehicle_Output> = [];
	let loading = true;
	let showAddModal = false;
	let showDeleteModal = false;
	let vehicleToDelete: Vehicle_Output | null = null;

	async function loadVehicles() {
		try {
			const response = await api.vehicle.getMyVehiclesVehicleMyGet();
			vehicles = response;
		} catch (error) {
			console.error('Failed to load vehicles:', error);
			toast.error('Failed to load vehicles');
		} finally {
			loading = false;
		}
	}

	// Subscribe to auth changes
	$: if (!$auth.loading && $auth.user) {
		loadVehicles();
	} else if (!$auth.loading && !$auth.user) {
		goto('/');
	}

	function handleVehicleAdded(vehicle: Vehicle_Output) {
		vehicles = [...vehicles, vehicle];
	}

	function handleDeleteClick({ detail }: CustomEvent<{ id: string }>) {
		const vehicle = vehicles.find((v) => v._id === detail.id);
		if (vehicle) {
			vehicleToDelete = vehicle;
			showDeleteModal = true;
		}
	}

	async function handleDeleteConfirm() {
		if (!vehicleToDelete) return;

		try {
			await api.vehicle.deleteVehicleVehicleVehicleIdDelete({
				vehicleId: vehicleToDelete._id
			});
			vehicles = vehicles.filter((v) => v._id !== vehicleToDelete?._id);
			toast.success('Vehicle deleted successfully');
		} catch (error) {
			console.error('Failed to delete vehicle:', error);
			toast.error('Failed to delete vehicle');
		} finally {
			showDeleteModal = false;
			vehicleToDelete = null;
		}
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-semibold text-gray-900">My Garage</h1>
		<button class="btn btn-primary" on:click={() => (showAddModal = true)}>
			<Plus class="h-4 w-4 mr-2" />
			Add Vehicle
		</button>
	</div>

	{#if $auth.loading || loading}
		<div class="flex justify-center py-12">
			<div class="animate-spin rounded-full h-8 w-8 border-t-2 border-primary-600" />
		</div>
	{:else if vehicles.length === 0}
		<div class="text-center py-12">
			<h3 class="mt-2 text-sm font-semibold text-gray-900">No vehicles</h3>
			<p class="mt-1 text-sm text-gray-500">Get started by adding your first vehicle.</p>
			<div class="mt-6">
				<button class="btn btn-primary" on:click={() => (showAddModal = true)}>
					<Plus class="h-4 w-4 mr-2" />
					Add Vehicle
				</button>
			</div>
		</div>
	{:else}
		<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
			{#each vehicles as vehicle (vehicle._id)}
				<VehicleCard {vehicle} on:delete={handleDeleteClick} />
			{/each}
		</div>
	{/if}
</div>

<AddVehicleModal bind:open={showAddModal} onAdd={handleVehicleAdded} />

<Modal
	title="Delete Vehicle"
	bind:open={showDeleteModal}
	on:close={() => {
		showDeleteModal = false;
		vehicleToDelete = null;
	}}
>
	{#if vehicleToDelete}
		<div class="space-y-4">
			<p class="text-gray-600">
				Are you sure you want to delete {vehicleToDelete.year}
				{vehicleToDelete.make}
				{vehicleToDelete.model}? This action cannot be undone.
			</p>
			<div class="flex justify-end space-x-3">
				<button
					type="button"
					class="btn btn-secondary"
					on:click={() => {
						showDeleteModal = false;
						vehicleToDelete = null;
					}}
				>
					Cancel
				</button>
				<button type="button" class="btn btn-danger" on:click={handleDeleteConfirm}>
					Delete Vehicle
				</button>
			</div>
		</div>
	{/if}
</Modal>
