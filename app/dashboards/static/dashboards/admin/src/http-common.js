import axios from 'axios';
import config from '@/config'


const instance = axios.create({
	baseURL: `http://${config.apiRoot}`
});
instance.defaults.xsrfCookieName = 'csrftoken';
instance.defaults.xsrfHeaderName = 'X-CSRFToken'

export default instance;