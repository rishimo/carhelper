<script lang="ts">
	import { api } from '@/lib/api';
	import Modal from './Modal.svelte';
	import { toast } from 'svelte-sonner';
	import type { Fuel_Input } from '@lib/generated';

	export let open = false;
	export let vehicleId: string;
	export let onAdd: () => void;

	let loading = false;
	let gallons = '';
	let cost = '';
	let mileage = '';
	let date = new Date().toISOString().split('T')[0];
	let notes = '';

	async function handleSubmit() {
		if (!gallons || !cost || !mileage || !date) {
			toast.error('Please fill in all required fields');
			return;
		}

		loading = true;
		try {
			const fuelRecord: Fuel_Input = {
				VIN: vehicleId,
				gallons: parseFloat(gallons),
				cost: parseFloat(cost),
				mileage: parseInt(mileage),
				date,
				notes: notes || undefined
			};

			await api.vehicle.addFuelRecordVehicleVehicleIdFuelPost({
				vehicleId,
				requestBody: fuelRecord
			});

			toast.success('Fuel record added successfully');
			onAdd();
			resetForm();
		} catch (error) {
			console.error('Failed to add fuel record:', error);
			toast.error('Failed to add fuel record');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		gallons = '';
		cost = '';
		mileage = '';
		date = new Date().toISOString().split('T')[0];
		notes = '';
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Add Fuel Record" bind:open on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="gallons" class="label">Gallons *</label>
			<input
				type="number"
				id="gallons"
				class="input"
				bind:value={gallons}
				placeholder="Gallons of fuel"
				step="0.001"
				min="0"
				required
			/>
		</div>

		<div>
			<label for="cost" class="label">Total Cost ($) *</label>
			<input
				type="number"
				id="cost"
				class="input"
				bind:value={cost}
				placeholder="Total cost"
				step="0.01"
				min="0"
				required
			/>
		</div>

		<div>
			<label for="mileage" class="label">Mileage *</label>
			<input
				type="number"
				id="mileage"
				class="input"
				bind:value={mileage}
				placeholder="Current mileage"
				required
			/>
		</div>

		<div>
			<label for="date" class="label">Date *</label>
			<input type="date" id="date" class="input" bind:value={date} required />
		</div>

		<div>
			<label for="notes" class="label">Notes</label>
			<textarea
				id="notes"
				class="input"
				bind:value={notes}
				placeholder="Additional notes"
				rows="3"
			/>
		</div>

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-white mr-2" />
				{/if}
				Add Fuel Record
			</button>
		</div>
	</form>
</Modal>
