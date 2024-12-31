import { writable } from 'svelte/store';
import { api } from '@lib/api';
import { OpenAPI } from '@lib/generated/core/OpenAPI';
import type { UserPrivateView, UserSignupInput, UserAuthInput } from '@lib/generated';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import { ApiError } from '@lib/generated/core/ApiError';

interface AuthState {
	user: UserPrivateView | null;
	token: string | null;
	loading: boolean;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		user: null,
		token: browser ? localStorage.getItem('token') : null,
		loading: true
	});

	async function initializeAuth() {
		if (browser) {
			const token = localStorage.getItem('token');
			if (token) {
				OpenAPI.HEADERS = {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				};
				try {
					const user = await api.user.getUserUserGet({ userId: 'me' });
					if (user && 'email' in user) {
						update((state) => ({ ...state, user: user as UserPrivateView, token, loading: false }));
						return;
					}
				} catch (error) {
					console.error('Failed to get user details:', error);
					localStorage.removeItem('token');
					OpenAPI.HEADERS = {
						'Content-Type': 'application/json'
					};
				}
			}
			update((state) => ({ ...state, loading: false }));
		}
	}

	// Initialize auth state
	initializeAuth();

	return {
		subscribe,
		setUser: (user: UserPrivateView | null) => update((state) => ({ ...state, user })),
		setToken: (token: string | null) => {
			if (browser) {
				if (token) {
					localStorage.setItem('token', token);
					OpenAPI.HEADERS = {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`
					};
				} else {
					localStorage.removeItem('token');
					OpenAPI.HEADERS = {
						'Content-Type': 'application/json'
					};
				}
			}
			update((state) => ({ ...state, token }));
		},
		setLoading: (loading: boolean) => update((state) => ({ ...state, loading })),
		login: async (email: string, password: string, rememberMe: boolean = false) => {
			try {
				// Login and get access token
				const loginResponse = await api.auth.loginAuthLoginPost({
					requestBody: { email, password, remember_me: rememberMe } as UserAuthInput
				});

				// The refresh token is now set as a cookie by the server
				// Set the access token in headers for future requests
				const token = loginResponse.access_token;
				OpenAPI.HEADERS = {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				};

				// Update store with token
				update((state) => ({ ...state, token }));

				try {
					// Get user details
					const user = await api.user.getUserUserGet({ userId: 'me' });
					if (user && 'email' in user) {
						update((state) => ({ ...state, user: user as UserPrivateView }));
					}
				} catch (error) {
					console.error('Failed to get user details:', error);
					set({ user: null, token: null, loading: false });
					throw error;
				}

				return loginResponse;
			} catch (error) {
				console.error('Login error:', error);
				set({ user: null, token: null, loading: false });
				throw error;
			}
		},
		register: async (userData: UserSignupInput) => {
			try {
				const response = await api.register.userRegistrationRegisterPost({ requestBody: userData });
				return response;
			} catch (error) {
				console.error('Registration error:', error);
				throw error;
			}
		},
		logout: async () => {
			try {
				// Call the logout endpoint to invalidate the refresh token
				await fetch('/auth/logout', { method: 'POST' });
			} catch (error) {
				console.error('Logout error:', error);
			} finally {
				if (browser) {
					localStorage.removeItem('token');
					OpenAPI.HEADERS = {
						'Content-Type': 'application/json'
					};
				}
				set({ user: null, token: null, loading: false });
				await goto('/');
			}
		}
	};
}

export const auth = createAuthStore();
