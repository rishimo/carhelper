<script lang="ts">
	import { Wrench, Fuel, DollarSign, Gauge } from 'lucide-svelte';

	export let data: Array<{
		type: 'service' | 'fuel' | 'expense' | 'odometer';
		date: string;
		data: any;
	}>;

	function getIcon(type: string) {
		switch (type) {
			case 'service':
				return Wrench;
			case 'fuel':
				return Fuel;
			case 'expense':
				return DollarSign;
			case 'odometer':
				return Gauge;
			default:
				return null;
		}
	}

	function formatDate(date: string) {
		return new Date(date).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function formatCurrency(amount: number) {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}
</script>

<div class="flow-root">
	<ul role="list" class="-mb-8">
		{#each data as event, idx}
			<li>
				<div class="relative pb-8">
					{#if idx !== data.length - 1}
						<span
							class="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"
							aria-hidden="true"
						/>
					{/if}
					<div class="relative flex space-x-3">
						<div>
							<span
								class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
								class:bg-blue-500={event.type === 'service'}
								class:bg-green-500={event.type === 'fuel'}
								class:bg-red-500={event.type === 'expense'}
								class:bg-gray-500={event.type === 'odometer'}
							>
								<svelte:component
									this={getIcon(event.type)}
									class="h-5 w-5 text-white"
									aria-hidden="true"
								/>
							</span>
						</div>
						<div class="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
							<div>
								<p class="text-sm text-gray-500">
									{#if event.type === 'service'}
										Service: {event.data.description}
										{#if event.data.cost}
											({formatCurrency(event.data.cost)})
										{/if}
									{:else if event.type === 'fuel'}
										Fuel: {event.data.units} gallons at {formatCurrency(
											event.data.price_per_unit
										)}/gal ({formatCurrency(event.data.cost)})
									{:else if event.type === 'expense'}
										Expense: {event.data.description}
										({formatCurrency(event.data.amount)})
									{:else if event.type === 'odometer'}
										Odometer reading: {event.data.reading.toLocaleString()} miles
									{/if}
								</p>
							</div>
							<div class="whitespace-nowrap text-right text-sm text-gray-500">
								<time datetime={event.date}>{formatDate(event.date)}</time>
							</div>
						</div>
					</div>
				</div>
			</li>
		{/each}
	</ul>
</div>
