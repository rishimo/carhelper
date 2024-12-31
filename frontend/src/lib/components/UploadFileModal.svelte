<script lang="ts">
	import { api } from '@lib/api';
	import Modal from './Modal.svelte';
	import { toasts } from '@stores/toast';

	export let open = false;
	export let vehicleId: string;
	export let onUpload: () => void;

	let file: File | null = null;
	let description = '';
	let uploading = false;

	async function handleSubmit() {
		if (!file) {
			toasts.error('Please select a file');
			return;
		}

		uploading = true;
		try {
			const formData = new FormData();
			formData.append('file', file);
			if (description) {
				formData.append('description', description);
			}

			await api.vehicle.uploadFileVehicleVehicleIdFilesPost({
				vehicleId,
				formData
			});

			toasts.success('File uploaded successfully');
			onUpload();
			open = false;
			resetForm();
		} catch (err) {
			console.error('Failed to upload file:', err);
			toasts.error('Failed to upload file');
		} finally {
			uploading = false;
		}
	}

	function handleFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.files && target.files.length > 0) {
			file = target.files[0];
		}
	}

	function resetForm() {
		file = null;
		description = '';
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Upload File" {open} on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="file" class="block text-sm font-medium text-gray-700">File</label>
			<input
				type="file"
				id="file"
				class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
				on:change={handleFileChange}
			/>
		</div>

		<div>
			<label for="description" class="block text-sm font-medium text-gray-700">Description</label>
			<input
				type="text"
				id="description"
				bind:value={description}
				class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
			/>
		</div>

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={uploading}>
				{#if uploading}
					<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-white mr-2" />
				{/if}
				Upload
			</button>
		</div>
	</form>
</Modal>
