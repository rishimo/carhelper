<script lang="ts">
	import { api } from '@lib/api';
	import Modal from './Modal.svelte';
	import { toasts } from '@stores/toast';
	import type { Service_Input } from '@lib/generated/core/Service';
	import type { ServiceItem_Input } from '@lib/generated/core/ServiceItem';
	import { ServiceType } from '@lib/generated/core/ServiceType';

	export let open = false;
	export let vehicleId: string;
	export let onAdd: () => void;

	let loading = false;
	let date = new Date().toISOString().split('T')[0];
	let items: Array<ServiceItem_Input> = [{ description: '', cost: 0 }];

	const serviceTypes = Object.values(ServiceType);

	function addItem() {
		items = [...items, { description: '', cost: 0 }];
	}

	function removeItem(index: number) {
		items = items.filter((_, i) => i !== index);
	}

	async function handleSubmit() {
		if (!date || items.some((item) => !item.description)) {
			toasts.error('Please fill in all required fields');
			return;
		}

		loading = true;
		try {
			const totalCost = items.reduce((sum, item) => sum + item.cost, 0);

			const serviceInput: Service_Input = {
				VIN: vehicleId,
				date,
				cost: totalCost,
				items
			};

			await api.vehicle.addServiceRecord({
				vehicleId,
				requestBody: serviceInput
			});

			toasts.success('Service record added successfully');
			onAdd();
			resetForm();
			open = false;
		} catch (err) {
			console.error('Failed to add service record:', err);
			toasts.error('Failed to add service record');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		date = new Date().toISOString().split('T')[0];
		items = [{ description: '', cost: 0 }];
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Add Service Record" {open} on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="date" class="block text-sm font-medium text-gray-700">Date</label>
			<input
				type="date"
				id="date"
				bind:value={date}
				class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
				required
			/>
		</div>

		<div class="space-y-4">
			<div class="flex justify-between items-center">
				<h4 class="text-sm font-medium text-gray-700">Service Items</h4>
				<button
					type="button"
					class="text-sm text-primary-600 hover:text-primary-500"
					on:click={addItem}
				>
					Add Item
				</button>
			</div>

			{#each items as item, i}
				<div class="flex gap-4">
					<div class="flex-grow">
						<label for="description-{i}" class="sr-only">Description</label>
						<input
							type="text"
							id="description-{i}"
							bind:value={item.description}
							placeholder="Description"
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
							required
						/>
					</div>
					<div class="w-32">
						<label for="cost-{i}" class="sr-only">Cost</label>
						<div class="relative">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<span class="text-gray-500 sm:text-sm">$</span>
							</div>
							<input
								type="number"
								id="cost-{i}"
								bind:value={item.cost}
								min="0"
								step="0.01"
								class="block w-full rounded-md border-gray-300 pl-7 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
								required
							/>
						</div>
					</div>
					<div class="w-48">
						<label for="type-{i}" class="sr-only">Type</label>
						<select
							id="type-{i}"
							bind:value={item.service_type}
							class="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
						>
							<option value={undefined}>Select type</option>
							{#each serviceTypes as type}
								<option value={type}>{type.replace(/_/g, ' ')}</option>
							{/each}
						</select>
					</div>
					{#if items.length > 1}
						<button
							type="button"
							class="text-gray-400 hover:text-red-500"
							on:click={() => removeItem(i)}
						>
							<svg
								class="h-5 w-5"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
									clip-rule="evenodd"
								/>
							</svg>
						</button>
					{/if}
				</div>
			{/each}
		</div>

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-white mr-2" />
				{/if}
				Add Service Record
			</button>
		</div>
	</form>
</Modal>
