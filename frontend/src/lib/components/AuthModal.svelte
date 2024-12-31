<script lang="ts">
	import { auth } from '../stores/auth';
	import Modal from './Modal.svelte';
	import toast from 'svelte-french-toast';
	import type { UserSignupInput } from '../generated/models';

	export let open = false;

	let loading = false;
	let isLogin = true;

	// Login form
	let loginEmail = '';
	let loginPassword = '';

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
		open = false;
		resetForm();
	}

	function resetForm() {
		loginEmail = '';
		loginPassword = '';
		registerEmail = '';
		registerPassword = '';
		registerConfirmPassword = '';
		registerUsername = '';
		registerFirstName = '';
		registerLastName = '';
		loading = false;
		passwordsMatch = true;
	}

	function validatePasswords() {
		passwordsMatch = registerPassword === registerConfirmPassword;
		return passwordsMatch;
	}

	async function handleLogin() {
		loading = true;

		try {
			await auth.login(loginEmail, loginPassword);
			toast.success('Logged in successfully');
			handleClose();
		} catch (error: any) {
			console.error('Login error:', error);
			if (error?.response?.data?.detail) {
				toast.error(error.response.data.detail);
			} else {
				toast.error('Invalid email or password');
			}
		} finally {
			loading = false;
		}
	}

	async function handleRegister() {
		if (!validatePasswords()) {
			toast.error('Passwords do not match');
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
			toast.success('Account created successfully! Please log in.');
			isLogin = true;
			resetForm();
		} catch (error: any) {
			console.error('Registration error:', error);
			if (error?.response?.data?.detail) {
				toast.error(error.response.data.detail);
			} else {
				toast.error('Failed to create account');
			}
		} finally {
			loading = false;
		}
	}
</script>

<Modal title={isLogin ? 'Login' : 'Create Account'} {open} on:close={handleClose}>
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

			<div class="flex justify-end space-x-3">
				<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
				<button type="submit" class="btn btn-primary" disabled={loading}>
					{#if loading}
						<div
							class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
						></div>
					{/if}
					Login
				</button>
			</div>

			<div class="text-center text-sm text-gray-600">
				Don't have an account?
				<button
					type="button"
					class="text-primary-600 hover:text-primary-700"
					on:click={() => (isLogin = false)}
				>
					Create one
				</button>
			</div>
		</form>
	{:else}
		<form on:submit|preventDefault={handleRegister} class="space-y-4">
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
					on:input={validatePasswords}
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
					class:border-red-500={!passwordsMatch}
					placeholder="Confirm your password"
					on:input={validatePasswords}
				/>
				{#if !passwordsMatch}
					<p class="mt-1 text-sm text-red-500">Passwords do not match</p>
				{/if}
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

			<div class="grid grid-cols-2 gap-4">
				<div>
					<label for="registerFirstName" class="label">First Name</label>
					<input
						type="text"
						id="registerFirstName"
						bind:value={registerFirstName}
						required
						class="input"
						placeholder="Enter your first name"
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
						placeholder="Enter your last name"
					/>
				</div>
			</div>

			<div class="flex justify-end space-x-3">
				<button type="button" class="btn btn-secondary" on:click={handleClose}>Cancel</button>
				<button type="submit" class="btn btn-primary" disabled={loading || !passwordsMatch}>
					{#if loading}
						<div
							class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
						></div>
					{/if}
					Create Account
				</button>
			</div>

			<div class="text-center text-sm text-gray-600">
				Already have an account?
				<button
					type="button"
					class="text-primary-600 hover:text-primary-700"
					on:click={() => (isLogin = true)}
				>
					Login
				</button>
			</div>
		</form>
	{/if}
</Modal>
