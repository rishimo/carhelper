<script lang="ts">
	import { toasts } from '@stores/toast';
	import { fly } from 'svelte/transition';
	import { theme } from '@lib/theme/colors';

	const TOAST_ICONS = {
		success: '✅',
		error: '❌',
		info: 'ℹ️'
	};
</script>

<div class="fixed top-4 left-1/2 -translate-x-1/2 z-50 space-y-2">
	{#each $toasts as toast (toast.id)}
		<div
			class="p-4 rounded-lg shadow-lg text-white flex items-center gap-2 whitespace-nowrap"
			style="background-color: {theme.notification}"
			transition:fly={{ y: -20, duration: 200 }}
		>
			<span class="text-lg">{TOAST_ICONS[toast.type]}</span>
			<span>{toast.message}</span>
		</div>
	{/each}
</div>
