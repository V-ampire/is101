import http from "@/core/services/http/common"

const endpoint = '/companies';

export default {

  list() {
    /**
     * Загрузить список юрлиц.
     */
    return http.get(endpoint)
  },

  detail(companyUuid) {
    /**
     * Загрузить информацю о юрлице.
     */
    return http.get(`${endpoint}/${companyUuid}`)
  },

	create(formData) {
    /**
     * Заполнить профиль юрлица.
     */
		const headers = {
			'Content-Type': 'multipart/form-data'
		};
		return http.post(endpoint, formData, {headers: headers})
  },
  
  update(companyUuid, formData) {
    /**
     * Обновить данные юрлица.
     */
    const headers = {
			'Content-Type': 'multipart/form-data'
		};
    return http.patch(`${endpoint}/${companyUuid}`, formData, {headers: headers})
  },

  delete(companyUuid) {
    /**
     * Удалить юрлицо. Будет удалена учетная запись.
     */
    return http.delete(`${endpoint}/${companyUuid}`)
  },

  toArchive(companyUuid, force=false) {
    /**
     * Переводит юрлицо в архи. Учетная запись будет отключена.
     * @param force - если не указан или false, то в случае если у юрлица числятся работники
     * с активным статусом - будет возвращена ошибка. Если true то все работники будут также 
     * переведены в архивный статус.
     */
    const headers = {
			'Content-Type': 'application/json'
    };
    return http.patch(`${endpoint}/${companyUuid}/to_archive`, {'force': force}, {headers: headers})
  },

  toWork(companyUuid) {
    /**
     * Переводит юрлицо в активный статус.
     */
    return http.patch(`${endpoint}/${companyUuid}/to_work`)
  }
}