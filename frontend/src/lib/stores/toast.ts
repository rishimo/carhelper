import { writable } from 'svelte/store';

interface Toast {
	id: number;
	message: string;
	type: 'success' | 'error' | 'info';
}

function createToastStore() {
	const { subscribe, update } = writable<Array<Toast>>([]);
	let id = 0;

	function show(message: string, type: 'success' | 'error' | 'info' = 'info') {
		const toast: Toast = {
			id: id++,
			message,
			type
		};

		update((toasts) => [...toasts, toast]);

		// Remove toast after 3 seconds
		setTimeout(() => {
			remove(toast.id);
		}, 3000);
	}

	function remove(id: number) {
		update((toasts) => toasts.filter((t) => t.id !== id));
	}

	return {
		subscribe,
		success: (message: string) => show(message, 'success'),
		error: (message: string) => show(message, 'error'),
		info: (message: string) => show(message)
	};
}

export const toasts = createToastStore();
