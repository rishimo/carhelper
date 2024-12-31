import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { fileURLToPath } from 'url';

export default defineConfig({
	plugins: [sveltekit()],
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url)),
			'@components': fileURLToPath(new URL('./src/lib/components', import.meta.url)),
			'@stores': fileURLToPath(new URL('./src/lib/stores', import.meta.url)),
			'@models': fileURLToPath(new URL('./src/lib/generated/models', import.meta.url)),
			'@services': fileURLToPath(new URL('./src/lib/generated/services', import.meta.url)),
			'@core': fileURLToPath(new URL('./src/lib/generated/core', import.meta.url)),
			'@utils': fileURLToPath(new URL('./src/lib/utils', import.meta.url))
		}
	}
});
