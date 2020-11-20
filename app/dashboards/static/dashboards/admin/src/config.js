const path = require('path')

const envPath = path.resolve('../', '.env');

require('dotenv').config({
	path: envPath
});

console.log(`api root: ${envPath}`);

export default {
	apiRoot: process.env.API_ROOT
}