import { generate } from 'openapi-typescript-codegen';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function generateApi() {
	await generate({
		input: resolve(__dirname, '../openapi.json'),
		output: resolve(__dirname, '../src/lib/generated'),
		client: 'axios',
		useOptions: true,
		useUnionTypes: true
	});
}

generateApi();
