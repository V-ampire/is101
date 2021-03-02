import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";

const endpoint = '/companies';

export default {

  list() {
    /**
     * Загрузить список юрлиц.
     */
    try {
      return http.get(`${endpoint}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  },

  detail(companyUuid) {
    /**
     * Загрузить информацю о юрлице.
     */
    try {
      return http.get(`${endpoint}/${companyUuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  },

	create(formData) {
    /**
     * Заполнить профиль юрлица.
     */
		const headers = {
			'Content-Type': 'multipart/form-data'
    };
    try {
      return http.post(`${endpoint}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  },
  
  update(companyUuid, formData) {
    /**
     * Обновить данные юрлица.
     */
    const headers = {
			'Content-Type': 'multipart/form-data'
    };
    try {
      return http.patch(`${endpoint}/${companyUuid}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  },

  delete(companyUuid) {
    /**
     * Удалить юрлицо. Будет удалена учетная запись.
     */
    try {
      return http.delete(`${endpoint}/${companyUuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
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
    try {
      return http.patch(`${endpoint}/${companyUuid}/to_archive/`, {'force': force}, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  },

  toWork(companyUuid) {
    /**
     * Переводит юрлицо в активный статус.
     */
    try {
      return http.patch(`${endpoint}/${companyUuid}/to_work/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
  }
}