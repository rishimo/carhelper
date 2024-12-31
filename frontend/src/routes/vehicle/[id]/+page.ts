import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { auth } from '@stores/auth';
import { get } from 'svelte/store';

export const load: PageLoad = async ({ params }) => {
	const authState = get(auth);
	console.log('Page load handler - auth state:', authState);

	if (!authState.token || !authState.user) {
		console.log('User not authenticated, redirecting to home');
		throw redirect(302, '/');
	}

	console.log('User authenticated, loading vehicle:', params.id);
	return {
		vehicleId: params.id
	};
};
