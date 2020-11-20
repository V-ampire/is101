import http from "@/http-common";

const endpoint = '/companies'

export default {

	fetchAll() {
		return http.get(endpoint).then(response => {
			return response.data
		});
	},

	create(data) {
		return http.post(endpoint, data);
	}
}