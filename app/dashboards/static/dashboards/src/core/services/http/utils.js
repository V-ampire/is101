import { ServerError, RequestError, SettingRequestError } from '@/core/errors'

export function processHttpError(error) {
  if (error.response) {
    throw new ServerError(error)
  } else if (error.request) {
    throw new RequestError(error)
  } else {
    throw new SettingRequestError(error)
  }
}