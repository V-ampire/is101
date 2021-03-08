import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";

const baseEndpoint = '/accounts';
const companiesEndpoint = `${baseEndpoint}/companies`;
const employeesEndpoint = `${baseEndpoint}/employees`;
const noProfilesEndpoint = `${baseEndpoint}/no_profiles`;

export default {

  companies: {

    async list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      let response;
      try {
        response = await http.get(`${companiesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async detail(accountUuid) {
      /**
       * Загрузить информацию об учетной записи.
       */
      let response;
      try {
        response = await http.get(`${companiesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.post(`${companiesEndpoint}/`, formData, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      let response;
      try {
        response = await http.patch(
          `${companiesEndpoint}/${accountUuid}/`, formData, {headers: headers}
        )
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
      
    },

    async delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      let response;
      try {
        response = await http.delete(`${companiesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      let response;
      try {
        response = await http.patch(`${companiesEndpoint}/${accountUuid}/activate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      let response;
      try {
        response = await http.patch(`${companiesEndpoint}/${accountUuid}/deactivate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.patch(
          `${companiesEndpoint}/${accountUuid}/change_password/`, 
          formData, 
          {'headers': headers})
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

  },

  employees: {

    async list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      let response;
      try {
        response = await http.get(`${employeesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async detail(accountUuid) {
      let response;
      try {
        response = await http.get(`${employeesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.post(`${employeesEndpoint}/`, formData, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.patch(
          `${employeesEndpoint}/${accountUuid}/`, formData, {headers: headers}
        )
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      let response;
      try {
        response = await http.delete(`${employeesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      let response;
      try {
        response = await http.patch(`${employeesEndpoint}/${accountUuid}/activate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      let response;
      try {
        response = await http.patch(`${employeesEndpoint}/${accountUuid}/deactivate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      let response;
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        response = await http.patch(
          `${employeesEndpoint}/${accountUuid}/change_password/`, 
          formData, 
          {'headers': headers})
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },
  },

  noProfiles: {

    async list() {
      /**
       * Возвращает список учетных записей юрлиц и работников с незаполеным профилем.
       */
      let response;
      try {
        response = await http.get(`${noProfilesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    },

    async count() {
      /**
       * Возвращает количество учетных записей юрлиц и работников с незаполеным профилем.
       */
      let response;
      try {
        response = await http.get(`${noProfilesEndpoint}/count/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      return response
    }
  }
}
