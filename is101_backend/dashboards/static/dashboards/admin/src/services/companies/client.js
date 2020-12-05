import http from "@/http-common"


class CompaniesApiClient {
	/*
	Клиент для работы с API юр. лиц
	*/
	constructor() {
		this.endpoint = '/companies/';
	}

	getAll() {
		return http.get(this.endpoint);
	}

	get(uuid) {
		return http.get(this.endpoint + uuid);
	}

	create(formData) {
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		return http.post(this.endpoint, formData, {headers: headers});
	}
	
	delete(uuid) {
		return http.delete(this.endpoint + uuid);
	}

	update(formData) {
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		return http.patch(this.endpoint, formData, {headers: headers});
	}

	archivate(uuid) {
		return http.get(this.endpoint + 'archivate/' + uuid);
	}

	activate(uuid) {
		return http.get(this.endpoint + 'activate/' + uuid);
	}
}

export default new CompaniesApiClient();