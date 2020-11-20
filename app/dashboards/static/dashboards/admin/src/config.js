const envPath = path.resolve('../', '.env');

const dotenv = require('dotenv').config({
	path: envPath
});


export default {
	apiRoot: process.env.API_ROOT
}