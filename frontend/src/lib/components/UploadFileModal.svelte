<script lang="ts">
	import { api } from '@lib/api';
	import Modal from '@components/Modal.svelte';
	import { toast } from 'svelte-sonner';
	import type { FileType } from '@lib/generated';

	export let open = false;
	export let vehicleId: string;
	export let onUpload: () => void;

	let loading = false;
	let file: File | null = null;
	let title = '';
	let fileType: FileType = FileType.RECEIPT;
	let description = '';

	async function handleSubmit() {
		if (!file || !title) {
			toast.error('Please select a file and enter a title');
			return;
		}

		loading = true;
		try {
			const formData = new FormData();
			formData.append('file', file);
			formData.append('title', title);
			formData.append('file_type', fileType);
			if (description) {
				formData.append('description', description);
			}

			await api.vehicle.uploadFileVehicleVehicleIdFilesPost({
				vehicleId,
				formData
			});

			toast.success('File uploaded successfully');
			onUpload();
			resetForm();
		} catch (error) {
			console.error('Failed to upload file:', error);
			toast.error('Failed to upload file');
		} finally {
			loading = false;
		}
	}

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files[0]) {
			file = input.files[0];
			if (!title) {
				title = file.name;
			}
		}
	}

	function resetForm() {
		file = null;
		title = '';
		fileType = FileType.RECEIPT;
		description = '';
	}

	function handleClose() {
		resetForm();
		open = false;
	}
</script>

<Modal title="Upload File" bind:open on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<label for="file" class="label">File *</label>
			<input
				type="file"
				id="file"
				class="input"
				on:change={handleFileChange}
				accept="image/*,application/pdf"
				required
			/>
		</div>

		<div>
			<label for="title" class="label">Title *</label>
			<input
				type="text"
				id="title"
				class="input"
				bind:value={title}
				placeholder="File title"
				required
			/>
		</div>

		<div>
			<label for="file-type" class="label">File Type</label>
			<select id="file-type" class="input" bind:value={fileType}>
				{#each Object.values(FileType) as type}
					<option value={type}>{type}</option>
				{/each}
			</select>
		</div>

		<div>
			<label for="description" class="label">Description</label>
			<textarea
				id="description"
				class="input"
				bind:value={description}
				placeholder="File description"
				rows="3"
			/>
		</div>

		<div class="flex justify-end space-x-3">
			<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-white mr-2" />
				{/if}
				Upload File
			</button>
		</div>
	</form>
</Modal>
