import http from "@/core/services/http/common"

const baseEndpoint = '/accounts';
const companiesEndpoint = `${baseEndpoint}/companies`;
const employeesEndpoint = `${baseEndpoint}/employees`;

export default {

  companies: {

    list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      return http.get(companiesEndpoint)
    },

    detail(accountUuid) {
      return http.get(`${companiesEndpoint}/${accountUuid}`)
    },

    create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      return http.post(companiesEndpoint, formData, {headers: headers})
    },

    update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      return http.patch(
        `${companiesEndpoint}/${accountUuid}`, formData, {headers: headers}
      )
    },

    delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      return http.delete(`${companiesEndpoint}/${accountUuid}`)
    },

    activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      return http.patch(`${companiesEndpoint}/${accountUuid}/activate`)
    },

    deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      return http.patch(`${companiesEndpoint}/${accountUuid}/deactivate`)
    },

    changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      return http.patch(`${companiesEndpoint}/${accountUuid}/change_password`)
    },

  },

  employees: {

    list() {
      /**
       * Загрузить список учетных записей юрлиц.
       */
      return http.get(employeesEndpoint)
    },

    detail(accountUuid) {
      return http.get(`${employeesEndpoint}/${accountUuid}`)
    },

    create(formData) {
      /**
       * Создать учетную запись юрлица.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      return http.post(employeesEndpoint, formData, {headers: headers})
    },

    update(accountUuid, formData) {
      /**
       * Обновить данные учетной записи.
       */
      const headers = {
        'Content-Type': 'multipart/form-data'
      };
      return http.patch(
        `${employeesEndpoint}/${accountUuid}`, formData, {headers: headers}
      )
    },

    delete(accountUuid) {
      /**
       * Удалить ученую запись.
       */
      return http.delete(`${employeesEndpoint}/${accountUuid}`)
    },

    activate(accountUuid) {
      /**
       * Перевести учетную запись в активный статус.
       */
      return http.patch(`${employeesEndpoint}/${accountUuid}/activate`)
    },

    deactivate(accountUuid) {
      /**
       * Перевести учетную запись в неактивный статус, доступ будет ограничен.
       */
      return http.patch(`${employeesEndpoint}/${accountUuid}/deactivate`)
    },

    changePassword(accountUuid, formData) {
      /**
       * Изменить пароль.
       * @param formData - должен содержать пароль и подтверждение пароля.
       */
      return http.patch(`${employeesEndpoint}/${accountUuid}/change_password`)
    }
  }
}
