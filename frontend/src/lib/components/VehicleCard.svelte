<script lang="ts">
	import type { Vehicle } from '$lib/generated/models';
	import { Car, Gauge, DollarSign, Calendar, Trash2 } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	export let vehicle: Vehicle;

	const dispatch = createEventDispatcher<{
		delete: { id: string };
	}>();

	$: currentMileage = vehicle.odometer_records?.length
		? vehicle.odometer_records[vehicle.odometer_records.length - 1].reading
		: 0;

	$: totalCost =
		vehicle.service_records?.reduce((acc: number, record) => acc + record.cost, 0) || 0;

	function handleDelete(e: MouseEvent) {
		e.preventDefault(); // Prevent navigation
		dispatch('delete', { id: vehicle.id });
	}
</script>

<a href={`/vehicle/${vehicle.id}`} class="block">
	<div class="card group hover:shadow-md transition-shadow">
		<div class="flex items-start justify-between">
			<div class="flex items-center space-x-3">
				<div class="rounded-lg bg-primary-50 p-3 group-hover:bg-primary-100 transition-colors">
					<Car class="h-6 w-6 text-primary-600" />
				</div>
				<div>
					<h3 class="font-semibold text-gray-900">
						{vehicle.year}
						{vehicle.make}
						{vehicle.model}
					</h3>
					<p class="text-sm text-gray-500">VIN: {vehicle.VIN}</p>
				</div>
			</div>
			<div class="flex items-center space-x-2">
				{#if vehicle.color}
					<span
						class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium capitalize"
						style="background-color: {vehicle.color}25; color: {vehicle.color}"
					>
						{vehicle.color}
					</span>
				{/if}
				<button
					class="p-1 text-gray-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
					on:click={handleDelete}
					title="Delete vehicle"
				>
					<Trash2 class="h-4 w-4" />
				</button>
			</div>
		</div>

		<div class="mt-6 grid grid-cols-3 gap-4 border-t border-gray-100 pt-4">
			<div class="flex items-center space-x-2">
				<Gauge class="h-4 w-4 text-gray-400" />
				<span class="text-sm text-gray-600">{currentMileage.toLocaleString()} miles</span>
			</div>

			<div class="flex items-center space-x-2">
				<DollarSign class="h-4 w-4 text-gray-400" />
				<span class="text-sm text-gray-600">${totalCost.toLocaleString()}</span>
			</div>

			<div class="flex items-center space-x-2">
				<Calendar class="h-4 w-4 text-gray-400" />
				<span class="text-sm text-gray-600">
					{#if vehicle.purchase_date}
						{new Date(vehicle.purchase_date).toLocaleDateString()}
					{:else}
						Not set
					{/if}
				</span>
			</div>
		</div>
	</div>
</a>
