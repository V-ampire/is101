import http from "@/core/services/http/common"

const endpoint = '/companies/';

export default {

  getAll() {
    return http.get(endpoint)
  },

	// get(company_uuid) {
		
	// }

	create(formData) {
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		return http.post(endpoint, formData, {headers: headers})
	},
	
	// delete(company_uuid) {
	// 	return http.delete(`${endpoint}${company_uuid}`)
	// },

	// patch
}