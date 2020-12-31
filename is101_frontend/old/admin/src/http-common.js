import axios from 'axios';
import config from '@/config'


const http = axios.create({
	baseURL: `http://${config.apiRoot}`
});
http.defaults.xsrfCookieName = 'csrftoken';
http.defaults.xsrfHeaderName = 'X-CSRFToken'

export default http;