<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Vehicle_Output } from '@lib/generated';
	import { goto } from '$app/navigation';
	import { Car, Gauge, Calendar, Clock } from 'lucide-svelte';
	import { theme } from '@lib/theme/colors';

	export let vehicle: Vehicle_Output;
	export let showIcon = true;

	function handleCardClick() {
		goto(`/vehicle/${vehicle._id}`);
	}

	// Calculate current mileage
	$: currentMileage = vehicle.odometer_records?.length
		? vehicle.odometer_records[vehicle.odometer_records.length - 1].reading
		: 0;

	// Get the most recent event
	$: lastEvent = (() => {
		const events = [
			...(vehicle.service_records || [])
				.filter((r) => r.date)
				.map((r) => ({ type: 'Service', date: new Date(r.date!) })),
			...(vehicle.fuel_records || [])
				.filter((r) => r.date)
				.map((r) => ({ type: 'Fuel', date: new Date(r.date!) })),
			...(vehicle.odometer_records || [])
				.filter((r) => r.date)
				.map((r) => ({ type: 'Odometer', date: new Date(r.date!) }))
		].sort((a, b) => b.date.getTime() - a.date.getTime());

		return events[0] || null;
	})();

	function formatDate(date: Date) {
		return date.toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
	}
</script>

<div
	class="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
	on:click={handleCardClick}
>
	<div class="flex items-start space-x-3">
		{#if showIcon}
			<div class="rounded-lg bg-primary-50 p-3 group-hover:bg-primary-100 transition-colors">
				<Car class="h-6 w-6" style="color: {theme.primary}" />
			</div>
		{/if}
		<div class="flex-grow">
			<h3 class="text-lg font-semibold text-gray-900">
				{vehicle.year}
				{vehicle.make}
				{vehicle.model}
			</h3>
			<p class="mt-1 text-sm text-gray-500">VIN: {vehicle.VIN}</p>

			<div class="mt-4 grid grid-cols-2 gap-4">
				<div class="flex items-center space-x-2">
					<Gauge class="h-4 w-4 text-gray-400" />
					<span class="text-sm text-gray-600">{currentMileage.toLocaleString()} miles</span>
				</div>

				{#if vehicle.purchase_date}
					<div class="flex items-center space-x-2">
						<Calendar class="h-4 w-4 text-gray-400" />
						<span class="text-sm text-gray-600">
							{formatDate(new Date(vehicle.purchase_date))}
						</span>
					</div>
				{/if}

				{#if lastEvent}
					<div class="flex items-center space-x-2 col-span-2">
						<Clock class="h-4 w-4 text-gray-400" />
						<span class="text-sm text-gray-600">
							Last {lastEvent.type}: {formatDate(lastEvent.date)}
						</span>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
