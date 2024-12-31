<script lang="ts">
	import { api } from '$lib/api';
	import Modal from './Modal.svelte';
	import toast from 'svelte-french-toast';
	import type { Service_Input } from '$lib/generated';

	export let open = false;
	export let vehicleId: string;
	export let onAdd: () => void;

	let loading = false;
	let title = '';
	let description = '';
	let cost = '';
	let mileage = '';
	let date = new Date().toISOString().split('T')[0];

	async function handleSubmit() {
		if (!title || !date || !cost || !mileage) {
			toast.error('Please fill in all required fields');
			return;
		}

		loading = true;
		try {
			const serviceRecord: Service_Input = {
				VIN: vehicleId,
				title,
				description: description || undefined,
				cost: parseFloat(cost),
				mileage: parseInt(mileage),
				date
			};

			await api.vehicle.addServiceRecordVehicleVehicleIdServicePost({
				vehicleId,
				requestBody: serviceRecord
			});

			toast.success('Service record added successfully');
			onAdd();
			resetForm();
		} catch (error) {
			console.error('Failed to add service record:', error);
			toast.error('Failed to add service record');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		title = '';
		description = '';
		cost = '';
		mileage = '';
		date = new Date().toISOString().split('T')[0];
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Add Service Record" bind:open on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="title" class="label">Title *</label>
			<input
				type="text"
				id="title"
				class="input"
				bind:value={title}
				placeholder="Service title"
				required
			/>
		</div>

		<div>
			<label for="description" class="label">Description</label>
			<textarea
				id="description"
				class="input"
				bind:value={description}
				placeholder="Service description"
				rows="3"
			/>
		</div>

		<div>
			<label for="cost" class="label">Cost ($) *</label>
			<input
				type="number"
				id="cost"
				class="input"
				bind:value={cost}
				placeholder="Service cost"
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

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-white mr-2" />
				{/if}
				Add Service
			</button>
		</div>
	</form>
</Modal>
