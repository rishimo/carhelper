import { writable } from 'svelte/store';
import { api } from '../api';
import { OpenAPI } from '../generated/core/OpenAPI';
import type { UserPrivateView, UserSignupInput } from '../generated/models';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';

interface AuthState {
	user: UserPrivateView | null;
	token: string | null;
	loading: boolean;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		user: null,
		token: browser ? localStorage.getItem('token') : null,
		loading: false
	});

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
		login: async (email: string, password: string) => {
			try {
				// Login and get access token
				const loginResponse = await api.auth.loginAuthLoginPost({
					requestBody: { email, password }
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
			if (browser) {
				localStorage.removeItem('token');
				OpenAPI.HEADERS = {
					'Content-Type': 'application/json'
				};
			}
			set({ user: null, token: null, loading: false });
			await goto('/');
		}
	};
}

export const auth = createAuthStore();
