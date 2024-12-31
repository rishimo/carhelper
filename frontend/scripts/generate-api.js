import { generate } from 'openapi-typescript-codegen';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function generateApi() {
	console.log('Pulling latest OpenAPI spec - make sure the server is running');
	await fetch('http://localhost:8000/openapi.json')
		.then((response) => response.json())
		.then(async () => {
			console.log('Generating API...');
			await generate({
				input: resolve(__dirname, '../openapi.json'),
				output: resolve(__dirname, '../src/lib/generated'),
				client: 'axios',
				useOptions: true,
				useUnionTypes: true
			});
			console.log('API generated successfully');
		})
		.catch((error) => {
			console.error('Error fetching OpenAPI spec:', error);
		});
	console.log('API generated successfully');
}

generateApi();
