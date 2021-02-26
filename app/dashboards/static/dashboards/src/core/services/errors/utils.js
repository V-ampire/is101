import { ServerError, RequestError, SettingRequestError } from '@/core/services/errors/types';
import eventUtils from '@/core/services/events/utils';

export function processHttpError(error) {
  /**
   * Обрабатывае ошибку при выполнении http запроса.
   */
  let httpError;
  if (error.response) {
    httpError = new ServerError(error);
  } else if (error.request) {
    httpError = new RequestError(error);
  } else {
    httpError = new SettingRequestError(error);
  }
  eventUtils.showErrorAlert(httpError.message);
  return httpError
}