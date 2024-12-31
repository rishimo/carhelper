<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import AuthModal from '$lib/components/AuthModal.svelte';
	import { Car } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	let showAuthModal = false;

	$: if ($auth.user) {
		goto('/garage');
	}
</script>

<div class="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center px-4 text-center">
	<Car class="h-16 w-16 text-primary-600" />
	<h1 class="mt-8 text-4xl font-bold tracking-tight text-gray-900">Welcome to carHelper</h1>
	<p class="mt-4 text-lg text-gray-600">
		Track your vehicle's service history, expenses, and more.
	</p>
	<div class="mt-8">
		<button class="btn btn-primary" on:click={() => (showAuthModal = true)}> Get Started </button>
	</div>

	<div class="mt-12 grid gap-8 sm:grid-cols-3">
		<div class="flex flex-col items-center">
			<div class="rounded-lg bg-primary-50 p-3">
				<Car class="h-6 w-6 text-primary-600" />
			</div>
			<h3 class="mt-4 text-lg font-semibold">Vehicle Management</h3>
			<p class="mt-2 text-sm text-gray-600">Keep track of all your vehicles in one place</p>
		</div>

		<div class="flex flex-col items-center">
			<div class="rounded-lg bg-primary-50 p-3">
				<Car class="h-6 w-6 text-primary-600" />
			</div>
			<h3 class="mt-4 text-lg font-semibold">Service History</h3>
			<p class="mt-2 text-sm text-gray-600">Log and track all maintenance and repairs</p>
		</div>

		<div class="flex flex-col items-center">
			<div class="rounded-lg bg-primary-50 p-3">
				<Car class="h-6 w-6 text-primary-600" />
			</div>
			<h3 class="mt-4 text-lg font-semibold">Expense Tracking</h3>
			<p class="mt-2 text-sm text-gray-600">Monitor fuel costs and other expenses</p>
		</div>
	</div>
</div>

<AuthModal bind:open={showAuthModal} />
