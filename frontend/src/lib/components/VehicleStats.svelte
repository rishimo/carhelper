<script lang="ts">
	import { Gauge, DollarSign, Wrench, Fuel } from 'lucide-svelte';

	export let stats: {
		current_mileage: number;
		total_cost_of_ownership: number;
		fuel_efficiency: number | null;
		total_service_records: number;
		total_fuel_records: number;
		total_expenses: number;
	};

	function formatCurrency(amount: number) {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}
</script>

<dl class="divide-y divide-gray-100">
	<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
		<dt class="text-sm font-medium text-gray-500 flex items-center">
			<Gauge class="h-4 w-4 mr-2" />
			Current Mileage
		</dt>
		<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
			{stats.current_mileage.toLocaleString()} miles
		</dd>
	</div>

	<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
		<dt class="text-sm font-medium text-gray-500 flex items-center">
			<DollarSign class="h-4 w-4 mr-2" />
			Total Cost of Ownership
		</dt>
		<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
			{formatCurrency(stats.total_cost_of_ownership)}
		</dd>
	</div>

	{#if stats.fuel_efficiency !== null}
		<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
			<dt class="text-sm font-medium text-gray-500 flex items-center">
				<Fuel class="h-4 w-4 mr-2" />
				Fuel Efficiency
			</dt>
			<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
				{stats.fuel_efficiency.toFixed(1)} MPG
			</dd>
		</div>
	{/if}

	<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
		<dt class="text-sm font-medium text-gray-500 flex items-center">
			<Wrench class="h-4 w-4 mr-2" />
			Service Records
		</dt>
		<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
			{stats.total_service_records} records
		</dd>
	</div>

	<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
		<dt class="text-sm font-medium text-gray-500 flex items-center">
			<Fuel class="h-4 w-4 mr-2" />
			Fuel Records
		</dt>
		<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
			{stats.total_fuel_records} records
		</dd>
	</div>

	<div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
		<dt class="text-sm font-medium text-gray-500 flex items-center">
			<DollarSign class="h-4 w-4 mr-2" />
			Other Expenses
		</dt>
		<dd class="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
			{stats.total_expenses} records
		</dd>
	</div>
</dl>
