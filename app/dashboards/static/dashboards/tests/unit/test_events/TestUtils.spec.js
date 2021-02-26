import utils from '@/core/services/events/utils'
import eventBus from '@/core/services/events/eventBus'
import { ON_APP_ERROR } from '@/core/services/events/types'

describe('Тест для утилит для работы с событиями', () => {

  it('Tecт функции showErrorAlert', () => {
    eventBus.$emit = jest.fn();
    const expectedMessge = 'Test error message'

    utils.showErrorAlert(expectedMessge);

    expect(eventBus.$emit).toHaveBeenCalledTimes(1);
    expect(eventBus.$emit).toHaveBeenCalledWith(ON_APP_ERROR, expectedMessge);
  });

  it('Тест для функции onErrorEvent', () => {
    eventBus.$on = jest.fn();
    const expectedHandler = jest.fn();

    utils.onErrorEvent(expectedHandler);

    expect(eventBus.$on).toHaveBeenCalledTimes(1);
    expect(eventBus.$on).toHaveBeenCalledWith(ON_APP_ERROR, expectedHandler);
  })
})