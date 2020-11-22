import http from "@/http-common"
//import Cookies from 'js-cookie';

const endpoint = '/companies/';


export default {

	fetchAll() {
		return http.get(endpoint).then(response => {
			return response.data
		});
	},

	create(data) {
		const formData = new FormData()
		for (let key in data) {
			formData.append(key, data[key])
		}
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		// const data = companyData;
		// data[user.username] = userData.username;
		// data[user.password] = userData.password;
		return http.post(endpoint, formData, {
			headers: headers,
		})
	}
}