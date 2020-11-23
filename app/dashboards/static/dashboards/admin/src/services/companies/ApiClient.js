import http from "@/http-common"
//import Cookies from 'js-cookie';

const endpoint = '/companies/';


export default {

	fetchAll() {
		return http.get(endpoint).then(response => {
			return response.data
		});
	},

	create(formData) {
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		return http.post(endpoint, formData, {
			headers: headers,
		})
	}
}