<script lang="ts">
	import { api } from '@/lib/api';
	import Modal from '@components/Modal.svelte';
	import toast from 'svelte-french-toast';
	import type { Vehicle_Output } from '@models';

	export let open = false;
	export let onAdd: (vehicle: Vehicle_Output) => void;

	let loading = false;
	let vin = '';
	let make = '';
	let model = '';
	let year = new Date().getFullYear();
	let color = '';
	let purchaseDate = '';
	let purchasePrice: number | undefined;

	function handleClose() {
		open = false;
		resetForm();
	}

	function resetForm() {
		vin = '';
		make = '';
		model = '';
		year = new Date().getFullYear();
		color = '';
		purchaseDate = '';
		purchasePrice = undefined;
		loading = false;
	}

	async function handleSubmit() {
		loading = true;

		try {
			const vehicle = await api.vehicle.createVehicleVehiclePost({
				requestBody: {
					VIN: vin,
					make,
					model,
					year,
					color: color || undefined,
					purchase_date: purchaseDate || undefined,
					purchase_price: purchasePrice
				}
			});

			toast.success('Vehicle added successfully');
			onAdd(vehicle);
			handleClose();
		} catch (error) {
			toast.error('Failed to add vehicle');
		} finally {
			loading = false;
		}
	}
</script>

<Modal title="Add Vehicle" {open} on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="vin" class="label">VIN</label>
			<input
				type="text"
				id="vin"
				bind:value={vin}
				required
				class="input uppercase"
				placeholder="Enter vehicle VIN"
			/>
		</div>

		<div class="grid grid-cols-2 gap-4">
			<div>
				<label for="make" class="label">Make</label>
				<input
					type="text"
					id="make"
					bind:value={make}
					required
					class="input"
					placeholder="e.g., Toyota"
				/>
			</div>

			<div>
				<label for="model" class="label">Model</label>
				<input
					type="text"
					id="model"
					bind:value={model}
					required
					class="input"
					placeholder="e.g., Camry"
				/>
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4">
			<div>
				<label for="year" class="label">Year</label>
				<input type="number" id="year" bind:value={year} required class="input" min="1900" />
			</div>

			<div>
				<label for="color" class="label">Color (optional)</label>
				<input type="text" id="color" bind:value={color} class="input" placeholder="e.g., Red" />
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4">
			<div>
				<label for="purchaseDate" class="label">Purchase Date (optional)</label>
				<input type="date" id="purchaseDate" bind:value={purchaseDate} class="input" />
			</div>

			<div>
				<label for="purchasePrice" class="label">Purchase Price (optional)</label>
				<input
					type="number"
					id="purchasePrice"
					bind:value={purchasePrice}
					class="input"
					min="0"
					step="0.01"
				/>
			</div>
		</div>

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					<div
						class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
					></div>
				{/if}
				Add Vehicle
			</button>
		</div>
	</form>
</Modal>
