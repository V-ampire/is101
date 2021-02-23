import Vuetify from 'vuetify'
import ErrorAlert from '@/admin/views/accounts/NoProfilesList'
import utils from '@/core/services/events/utils'
import accounts from '@/core/services/http/accounts';

import { createLocalVue, shallowMount } from '@vue/test-utils';


describe('Тест NoProfilesList.vue', () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест вызова окна с ошибкой при неожиданном ответе сервера', done => {
    const resp = {data: 'Unexpected response.'};

    utils.showErrorAlert = jest.fn();
    accounts.noProfiles.list = jest.fn().mockResolvedValue(resp);

    const expectedMessage = 'Не удалось загрузить данные с сервера.';

    const wrapper = shallowMount(ErrorAlert, {
      localVue,
      vuetify,
    });

    setTimeout(() => {
      expect(utils.showErrorAlert).toHaveBeenCalledTimes(1);
      expect(utils.showErrorAlert).toHaveBeenCalledWith(expectedMessage);
      done();  
    }, 2000);

    
  });
});