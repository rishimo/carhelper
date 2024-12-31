<script lang="ts">
	import { api } from '@/lib/api';
	import Modal from '@components/Modal.svelte';
	import { toast } from 'svelte-sonner';
	import type { OdometerReading } from '@models/OdometerReading';

	export let open = false;
	export let vehicleId: string;
	export let onAdd: () => void;

	let loading = false;
	let reading = '';
	let notes = '';

	async function handleSubmit() {
		if (!reading) {
			toast.error('Please enter the odometer reading');
			return;
		}

		loading = true;
		try {
			const odometerReading: OdometerReading = {
				VIN: vehicleId,
				reading: parseInt(reading),
				notes: notes || undefined
			};

			await api.vehicle.addOdometerReadingVehicleVehicleIdOdometerPost({
				vehicleId,
				requestBody: odometerReading
			});

			toast.success('Odometer reading added successfully');
			onAdd();
			resetForm();
		} catch (error) {
			console.error('Failed to add odometer reading:', error);
			toast.error('Failed to add odometer reading');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		reading = '';
		notes = '';
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Add Odometer Reading" bind:open on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="reading" class="label">Reading (miles) *</label>
			<input
				type="number"
				id="reading"
				class="input"
				bind:value={reading}
				placeholder="Current odometer reading"
				required
			/>
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
				Add Reading
			</button>
		</div>
	</form>
</Modal>
