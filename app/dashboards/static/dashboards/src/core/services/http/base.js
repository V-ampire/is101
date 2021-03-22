import http from "@/core/services/http/common";
import errorUtils from "@/core/services/errors/utils";


export class ApiClient {
  /**
   * Базовый класс для api клиента.
   * Содержит методы: [
   *  list()
   *  detail()
   *  create()
   *  update()
   *  delete()
   *  toArchive()
   *  toWork()
   * ]
   */
  constructor(endpoint) {
    /**
     * @endpoint - ресурс объекта
     */
    this.endpoint = endpoint;
  }

  async list() {
    /**
     * Загрузить список объектов.
     */
    let response;
    try {
      response = await http.get(`${this.endpoint}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async detail(uuid) {
    /**
     * Загрузить информацю об объекте.
     */
    let response;
    try {
      response = await http.get(`${this.endpoint}/${uuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async create(formData) {
    /**
     * Создать объект.
     */
    let response;
    const headers = {
      'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.post(`${this.endpoint}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async update(uuid, formData) {
    /**
     * Обновить данные объекта.
     */
    let response;
    const headers = {
      'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.patch(`${this.endpoint}/${uuid}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async delete(uuid) {
    /**
     * Удалить объект.
     */
    let response;
    try {
      response = await http.delete(`${this.endpoint}/${uuid}/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async toArchive(uuid, force=false) {
    /**
     * Переводит объект в архив.
     * @param force - режим перевода в архив. При force=true все зависимые объекты также переводятся в архив.
     */
    let response;
    const headers = {
      'Content-Type': 'application/json'
    };
    try {
      response = await http.patch(`${this.endpoint}/${uuid}/to_archive/`, {'force': force}, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async toWork(uuid) {
    /**
     * Переводит объект в активный статус.
     */
    let response;
    try {
      response = await http.patch(`${this.endpoint}/${uuid}/to_work/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }
}


export class EmployeeApiClient extends ApiClient {
  /**
   * Клиент для API работников.
   * Определяет дополнительные методы: [
   *  changePosition()
   *  changeBranch()
   * ]
   */
  async changePosition(employeeUuid, formData) {
    /**
     * Меняет должность работника.
     */
    let response;
    const headers = {
      'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.patch(`${this.endpoint}/${employeeUuid}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async changeBranch(employeeUuid, formData) {
    /**
     * Переводит работника в другой филиал.
     */
    let response;
    const headers = {
      'Content-Type': 'multipart/form-data'
    };
    try {
      response = await http.patch(`${this.endpoint}/${employeeUuid}/`, formData, {headers: headers})
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }
}


export class PositionsClient extends ApiClient {
  /**
   * Клиент для API должностей.
   * Добавляет в метод list() возможность фильтрации по статусу.
   */
  async list(status=null) {
    if (!status) {
      return super.list()
    }
    let response;
    try {
      response = await http.get(`${this.endpoint}/?status=${status}`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }
}


export class AccountsClient extends ApiClient {
  /**
   * Клиент для API учетных записей.
   * Определяет дополнительные методы: [
   *  activate() - разрешает доступ учетной записи
   *  deactivate() - запрещает доступ учетной записи
   *  change_password() - меняет пароль учетной записи
   * ]
   */
  async activate(accountUuid) {
    let response;
    try {
      response = await http.patch(`${this.endpoint}/${accountUuid}/activate/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

  async desactivate(accountUuid) {
    let response;
    try {
      response = await http.patch(`${this.endpoint}/${accountUuid}/deactivate/`)
    } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }

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
        `${this.endpoint}/${accountUuid}/change_password/`, 
        formData, 
        {'headers': headers})
      } catch (err) {
      throw errorUtils.checkHttpError(err)
    }
    return response
  }
}