import { processHttpError } from '@/core/services/errors/utils';
import { ServerError, RequestError, SettingRequestError } from '@/core/services/errors/types';
import eventUtils from '@/core/services/events/utils';


describe('Тест функции processHttpError', () => {

  beforeEach(() => {
    // jest.spyOn(eventUtils, 'showErrorAlert');
    eventUtils.showErrorAlert = jest.fn();
  });

  it('Тест для серверной ошибки', () => {
    
    const expectedError = {response: 'testResponse'};

    const result = processHttpError(expectedError);

    expect(result).toBeInstanceOf(ServerError);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledTimes(1);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledWith(result.message);
  });

  it('Тест для ошибки при запросе', () => {

    const expectedError = {request: 'testRequest'};

    const result = processHttpError(expectedError);

    expect(result).toBeInstanceOf(RequestError);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledTimes(1);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledWith(result.message);
  });

  it('Тест ошибки клиента при отправке', () => {

    const expectedError = {info: 'testError'};

    const result = processHttpError(expectedError);

    expect(result).toBeInstanceOf(SettingRequestError);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledTimes(1);
    expect(eventUtils.showErrorAlert).toHaveBeenCalledWith(result.message);
  })
})

