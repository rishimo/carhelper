<script lang="ts">
	import { api } from '@/lib/api';
	import Modal from '@components/Modal.svelte';
	import { toast } from 'svelte-sonner';
	import type { Expense_Input } from '@models/Expense_Input';
	import { ExpenseType } from '@models/ExpenseType';

	export let open = false;
	export let vehicleId: string;
	export let onAdd: () => void;

	let loading = false;
	let description = '';
	let amount = '';
	let expenseType = ExpenseType.OTHER;
	let location = '';
	let notes = '';

	async function handleSubmit() {
		if (!description || !amount) {
			toast.error('Please fill in all required fields');
			return;
		}

		loading = true;
		try {
			const expense: Expense_Input = {
				VIN: vehicleId,
				description,
				amount: parseFloat(amount),
				expense_type: expenseType,
				location: location || undefined,
				notes: notes || undefined
			};

			await api.vehicle.addExpenseVehicleVehicleIdExpensePost({
				vehicleId,
				requestBody: expense
			});

			toast.success('Expense added successfully');
			onAdd();
			resetForm();
		} catch (error) {
			console.error('Failed to add expense:', error);
			toast.error('Failed to add expense');
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		description = '';
		amount = '';
		expenseType = ExpenseType.OTHER;
		location = '';
		notes = '';
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Add Expense" bind:open on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="expense-type" class="label">Expense Type</label>
			<select id="expense-type" class="input" bind:value={expenseType}>
				{#each Object.values(ExpenseType) as type}
					<option value={type}>{type}</option>
				{/each}
			</select>
		</div>

		<div>
			<label for="description" class="label">Description *</label>
			<input
				type="text"
				id="description"
				class="input"
				bind:value={description}
				placeholder="Registration, insurance, etc."
				required
			/>
		</div>

		<div>
			<label for="amount" class="label">Amount *</label>
			<input
				type="number"
				id="amount"
				class="input"
				bind:value={amount}
				placeholder="Amount in dollars"
				step="0.01"
				required
			/>
		</div>

		<div>
			<label for="location" class="label">Location</label>
			<input
				type="text"
				id="location"
				class="input"
				bind:value={location}
				placeholder="Where the expense occurred"
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
				Add Expense
			</button>
		</div>
	</form>
</Modal>
