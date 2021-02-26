import Vuetify from 'vuetify'
import ErrorAlert from '@/core/components/commons/ErrorAlert'
import utils from '@/core/services/events/utils'

import { createLocalVue, shallowMount } from '@vue/test-utils'


describe('Тест ErrorAlert.vue', () => {

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест действий при монтировании', () => {

    utils.onErrorEvent = jest.fn();

    const wrapper = shallowMount(ErrorAlert, {
      localVue,
      vuetify,
    });

    expect(utils.onErrorEvent).toHaveBeenCalledTimes(1);
    expect(utils.onErrorEvent).toHaveBeenCalledWith(wrapper.vm.open);
  });

  it('Тест метода open', () => {
    const wrapper = shallowMount(ErrorAlert, {
        localVue,
        vuetify,
    });
    const expected_message = 'Test message';

    wrapper.vm.open(expected_message);

    expect(wrapper.vm.showAlert = true);
    expect(wrapper.vm.message = expected_message);
});
})