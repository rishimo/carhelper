<script lang="ts">
	import { auth } from '@stores/auth';
	import Modal from '@components/Modal.svelte';
	import { toasts } from '@stores/toast';
	import type { UserSignupInput } from '@lib/generated';
	import { ApiError } from '@lib/generated/core/ApiError';
	import { onMount } from 'svelte';

	onMount(() => {
		toasts.info('Auth modal mounted');
	});

	export let open = false;

	let loading = false;
	let isLogin = true;

	// Login form
	let loginEmail = '';
	let loginPassword = '';
	let rememberMe = false;

	// Register form
	let registerEmail = '';
	let registerPassword = '';
	let registerConfirmPassword = '';
	let registerUsername = '';
	let registerFirstName = '';
	let registerLastName = '';

	// Form validation
	let passwordsMatch = true;

	function handleClose() {
		resetForm();
		open = false;
	}

	function resetForm() {
		loginEmail = '';
		loginPassword = '';
		rememberMe = false;
		registerEmail = '';
		registerPassword = '';
		registerConfirmPassword = '';
		registerUsername = '';
		registerFirstName = '';
		registerLastName = '';
		loading = false;
		passwordsMatch = true;
		isLogin = true;
	}

	function validatePasswords() {
		passwordsMatch = registerPassword === registerConfirmPassword;
		return passwordsMatch;
	}

	async function handleLogin() {
		loading = true;

		try {
			await auth.login(loginEmail, loginPassword, rememberMe);
			toasts.success('Logged in successfully');
			handleClose();
		} catch (error) {
			console.error('Login error:', error);
			if (error instanceof ApiError) {
				const message = error.body?.detail || error.message || 'Invalid email or password';
				toasts.error(message);
			} else if (error instanceof Error) {
				toasts.error(error.message || 'Failed to log in. Please try again.');
			} else {
				toasts.error('Failed to log in. Please try again.');
			}
		} finally {
			loading = false;
		}
	}

	async function handleRegister() {
		if (!validatePasswords()) {
			toasts.error('Passwords do not match');
			return;
		}

		loading = true;

		try {
			const userData: UserSignupInput = {
				email: registerEmail,
				password: registerPassword,
				username: registerUsername,
				first_name: registerFirstName,
				last_name: registerLastName
			};

			await auth.register(userData);
			toasts.success('Account created successfully! Please log in.');
			isLogin = true;
			resetForm();
		} catch (error) {
			console.error('Registration error:', error);
			if (error instanceof ApiError) {
				const message = error.body?.detail || error.message || 'Failed to create account';
				toasts.error(message);
			} else if (error instanceof Error) {
				toasts.error(error.message || 'Failed to create account. Please try again.');
			} else {
				toasts.error('Failed to create account. Please try again.');
			}
		} finally {
			loading = false;
		}
	}
</script>

<Modal title={isLogin ? 'Login' : 'Create Account'} bind:open on:close={resetForm}>
	{#if isLogin}
		<form on:submit|preventDefault={handleLogin} class="space-y-4">
			<div>
				<label for="loginEmail" class="label">Email</label>
				<input
					type="email"
					id="loginEmail"
					bind:value={loginEmail}
					required
					class="input"
					placeholder="Enter your email"
				/>
			</div>

			<div>
				<label for="loginPassword" class="label">Password</label>
				<input
					type="password"
					id="loginPassword"
					bind:value={loginPassword}
					required
					class="input"
					placeholder="Enter your password"
				/>
			</div>

			<div class="flex items-center">
				<input
					type="checkbox"
					id="rememberMe"
					bind:checked={rememberMe}
					class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
				/>
				<label for="rememberMe" class="ml-2 block text-sm text-gray-900">Remember me</label>
			</div>

			<div class="flex flex-col space-y-4">
				<button type="submit" class="btn btn-primary w-full" disabled={loading}>
					{#if loading}
						<div
							class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
						/>
					{/if}
					Login
				</button>
				<button
					type="button"
					class="text-sm text-gray-600 hover:text-gray-900"
					on:click={() => (isLogin = false)}
				>
					Don't have an account? Sign up
				</button>
			</div>
		</form>
	{:else}
		<form on:submit|preventDefault={handleRegister} class="space-y-4">
			<div class="grid grid-cols-2 gap-4">
				<div>
					<label for="registerFirstName" class="label">First Name</label>
					<input
						type="text"
						id="registerFirstName"
						bind:value={registerFirstName}
						required
						class="input"
						placeholder="First name"
					/>
				</div>

				<div>
					<label for="registerLastName" class="label">Last Name</label>
					<input
						type="text"
						id="registerLastName"
						bind:value={registerLastName}
						required
						class="input"
						placeholder="Last name"
					/>
				</div>
			</div>

			<div>
				<label for="registerUsername" class="label">Username</label>
				<input
					type="text"
					id="registerUsername"
					bind:value={registerUsername}
					required
					class="input"
					placeholder="Choose a username"
				/>
			</div>

			<div>
				<label for="registerEmail" class="label">Email</label>
				<input
					type="email"
					id="registerEmail"
					bind:value={registerEmail}
					required
					class="input"
					placeholder="Enter your email"
				/>
			</div>

			<div>
				<label for="registerPassword" class="label">Password</label>
				<input
					type="password"
					id="registerPassword"
					bind:value={registerPassword}
					required
					class="input"
					placeholder="Choose a password"
				/>
			</div>

			<div>
				<label for="registerConfirmPassword" class="label">Confirm Password</label>
				<input
					type="password"
					id="registerConfirmPassword"
					bind:value={registerConfirmPassword}
					required
					class="input"
					placeholder="Confirm your password"
				/>
			</div>

			<div class="flex flex-col space-y-4">
				<button type="submit" class="btn btn-primary w-full" disabled={loading}>
					{#if loading}
						<div
							class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
						/>
					{/if}
					Create Account
				</button>
				<button
					type="button"
					class="text-sm text-gray-600 hover:text-gray-900"
					on:click={() => (isLogin = true)}
				>
					Already have an account? Log in
				</button>
			</div>
		</form>
	{/if}
</Modal>
