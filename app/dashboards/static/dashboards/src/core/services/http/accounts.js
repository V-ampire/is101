import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";

const baseEndpoint = '/accounts';
const companiesEndpoint = `${baseEndpoint}/companies`;
const employeesEndpoint = `${baseEndpoint}/employees`;
const noProfilesEndpoint = `${baseEndpoint}/no_profiles`;

export default {

  companies: {

    list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      try {
        return http.get(`${companiesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    detail(accountUuid) {
      /**
       * Загрузить информацию об учетной записи.
       */
      try {
        return http.get(`${companiesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.post(`${companiesEndpoint}/`, formData, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.patch(
          `${companiesEndpoint}/${accountUuid}/`, formData, {headers: headers}
        )
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
      
    },

    delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      try {
        return http.delete(`${companiesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      try {
        return http.patch(`${companiesEndpoint}/${accountUuid}/activate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      try {
        return http.patch(`${companiesEndpoint}/${accountUuid}/deactivate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.patch(
          `${companiesEndpoint}/${accountUuid}/change_password/`, 
          formData, 
          {'headers': headers})
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

  },

  employees: {

    list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      try {
        return http.get(`${employeesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    detail(accountUuid) {
      try {
        return http.get(`${employeesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.post(`${employeesEndpoint}/`, formData, {headers: headers})
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.patch(
          `${employeesEndpoint}/${accountUuid}/`, formData, {headers: headers}
        )
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      try {
        return http.delete(`${employeesEndpoint}/${accountUuid}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      try {
        return http.patch(`${employeesEndpoint}/${accountUuid}/activate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      try {
        return http.patch(`${employeesEndpoint}/${accountUuid}/deactivate/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      try {
        return http.patch(
          `${employeesEndpoint}/${accountUuid}/change_password/`, 
          formData, 
          {'headers': headers})
        } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },
  },

  noProfiles: {

    list() {
      /**
       * Возвращает список учетных записей юрлиц и работников с незаполеным профилем.
       */
      try {
        return http.get(`${noProfilesEndpoint}/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    },

    count() {
      /**
       * Возвращает количество учетных записей юрлиц и работников с незаполеным профилем.
       */
      try {
        return http.get(`${noProfilesEndpoint}/count/`)
      } catch (err) {
        throw errorUtils.checkHttpError(err)
      }
    }
  }
}
