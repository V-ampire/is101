import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";

const endpoint = '/companies';

export default {

  async list() {
    /**
     * Загрузить список юрлиц.
     */
    let response;
    try {
      response = await http.get(`${endpoint}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },

  async detail(companyUuid) {
    /**
     * Загрузить информацю о юрлице.
     */
    let response;
    try {
      response = await http.get(`${endpoint}/${companyUuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },

	async create(formData) {
    /**
     * Заполнить профиль юрлица.
     */
    let response;
		const headers = {
			'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.post(`${endpoint}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },
  
  async update(companyUuid, formData) {
    /**
     * Обновить данные юрлица.
     */
    let response;
    const headers = {
			'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.patch(`${endpoint}/${companyUuid}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },

  async delete(companyUuid) {
    /**
     * Удалить юрлицо. Будет удалена учетная запись.
     */
    let response;
    try {
      response = await http.delete(`${endpoint}/${companyUuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },

  async toArchive(companyUuid, force=false) {
    /**
     * Переводит юрлицо в архи. Учетная запись будет отключена.
     * @param force - если не указан или false, то в случае если у юрлица числятся работники
     * с активным статусом - будет возвращена ошибка. Если true то все работники будут также 
     * переведены в архивный статус.
     */
    let response;
    const headers = {
			'Content-Type': 'application/json'
    };
    try {
      response = await http.patch(`${endpoint}/${companyUuid}/to_archive/`, {'force': force}, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  },

  async toWork(companyUuid) {
    /**
     * Переводит юрлицо в активный статус.
     */
    let response;
    try {
      response = await http.patch(`${endpoint}/${companyUuid}/to_work/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }
}