<script lang="ts">
	import { X } from 'lucide-svelte';
	import { fade, scale } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	export let title: string;
	export let open = false;

	const dispatch = createEventDispatcher<{
		close: void;
	}>();

	function handleClose() {
		open = false;
		dispatch('close');
	}

	function handleEscape(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			handleClose();
		}
	}

	function handleBackdropKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			handleClose();
		}
	}
</script>

<svelte:window on:keydown={handleEscape} />

{#if open}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0"
		in:fade={{ duration: 150 }}
		out:fade={{ duration: 150 }}
	>
		<div
			class="fixed inset-0 bg-gray-900/50"
			role="button"
			tabindex="0"
			on:click={handleClose}
			on:keydown={handleBackdropKeydown}
		></div>
		<div
			class="relative w-full max-w-lg rounded-lg bg-white p-8 shadow-lg sm:w-full"
			in:scale={{ duration: 150, start: 0.95 }}
			out:scale={{ duration: 150, start: 1 }}
		>
			<div class="flex items-center justify-between">
				<h2 class="text-xl font-semibold">{title}</h2>
				<button
					class="rounded-lg p-2.5 text-gray-500 hover:bg-gray-100 hover:text-gray-700"
					on:click={handleClose}
				>
					<X class="h-5 w-5" />
				</button>
			</div>
			<div class="mt-8">
				<slot />
			</div>
		</div>
	</div>
{/if}
