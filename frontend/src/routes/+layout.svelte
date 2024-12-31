<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { auth } from '@stores/auth';
	import { Car, UserCircle2, LogOut } from 'lucide-svelte';
	import { toasts } from '@stores/toast';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import Toast from '@components/Toast.svelte';

	let mounted = false;

	onMount(() => {
		mounted = true;
	});

	function logout() {
		auth.logout();
		toasts.success('Logged out successfully');
	}
</script>

<div class="app">
	{#if $auth.loading}
		<div class="flex items-center justify-center min-h-screen">
			<div class="animate-spin rounded-full h-8 w-8 border-t-2 border-primary-600"></div>
		</div>
	{:else}
		<div class="min-h-screen">
			{#if $auth.user}
				<nav class="bg-white shadow">
					<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
						<div class="flex justify-between h-16">
							<div class="flex">
								<a href="/" class="flex items-center px-2 text-primary-600 font-semibold text-lg">
									carHelper
								</a>
								<div class="hidden sm:ml-6 sm:flex sm:space-x-8">
									<a
										href="/garage"
										class:active={$page.url.pathname === '/garage'}
										class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 border-b-2 border-transparent hover:border-primary-500"
									>
										<Car class="w-4 h-4 mr-2" />
										My Garage
									</a>
								</div>
							</div>
							<div class="flex items-center">
								<div class="hidden sm:ml-6 sm:flex sm:items-center">
									<div class="relative ml-3">
										<div class="flex items-center space-x-4">
											<a
												href="/profile"
												class:active={$page.url.pathname === '/profile'}
												class="text-gray-500 hover:text-gray-700"
											>
												<UserCircle2 class="w-5 h-5" />
											</a>
											<button on:click={logout} class="text-gray-500 hover:text-gray-700">
												<LogOut class="w-5 h-5" />
											</button>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</nav>
			{/if}

			<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
				<slot />
			</main>
		</div>
	{/if}
</div>

{#if browser}
	<Toast />
{/if}

<style>
	.active {
		@apply border-primary-500 text-gray-900;
	}
</style>
