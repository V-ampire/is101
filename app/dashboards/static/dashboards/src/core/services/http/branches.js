import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";

export default function branchesApi(companyUuid) {

  const endpoint = `/companies/${companyUuid}/branches`;

  return {
    async list() {
      /**
       * Загрузить список филиалов.
       */
      let response;
      try {
        response = await http.get(`${endpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async detail(branchUuid) {
      /**
       * Загрузить информацю о филиале.
       */
      let response;
      try {
        response = await http.get(`${endpoint}/${branchUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async create(formData) {
      /**
       * Заполнить информацию о филиале.
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

    async update(branchUuid, formData) {
      /**
       * Обновить данные филиала.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.patch(`${endpoint}/${branchUuid}/`, formData, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },
  
    async delete(branchUuid) {
      /**
       * Удалить филиал. Будут удалены все работники филиала.
       */
      let response;
      try {
        response = await http.delete(`${endpoint}/${branchUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },
  
    async toArchive(branchUuid, force=false) {
      /**
       * Переводит филиал в архив.
       * @param force - если не указан или false, то в случае если в филиале числятся работники
       * с активным статусом - будет возвращена ошибка. Если true то все работники будут также 
       * переведены в архивный статус.
       */
      let response;
      const headers = {
        'Content-Type': 'application/json'
      };
      try {
        response = await http.patch(`${endpoint}/${branchUuid}/to_archive/`, {'force': force}, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },
  
    async toWork(branchUuid) {
      /**
       * Переводит филиал в активный статус.
       */
      let response;
      try {
        response = await http.patch(`${endpoint}/${branchUuid}/to_work/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    }
  }
}