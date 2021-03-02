import { ServerError, RequestError, SettingRequestError } from '@/core/services/errors/types';

export default {
  checkHttpError(error) {
    /**
     * Обрабатывает ошибку при выполнении http запроса.
     * Возвращает объект нужного класса http ошибки.
     */
    let httpError;
    if (error.response) {
      httpError = new ServerError(error);
    } else if (error.request) {
      httpError = new RequestError(error);
    } else {
      httpError = new SettingRequestError(error);
    }
    return httpError
  }
}