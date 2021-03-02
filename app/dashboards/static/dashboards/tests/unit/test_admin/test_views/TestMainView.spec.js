import Vuetify from 'vuetify'
import accounts from '@/core/services/http/accounts';
import Main from '@/admin/views/Main';
import router from '@/admin/router';
import VueRouter from 'vue-router'

import { createLocalVue, shallowMount } from '@vue/test-utils';
import faker from 'faker';
import flushPromises from 'flush-promises';



describe('Тест для отображения главной страницы админки для админов', () => {

  const expectedCount = faker.random.number();
  const expectedResponse = {data: {count: expectedCount}}
  const mockCount = jest.spyOn(accounts.noProfiles, 'count')
                      .mockResolvedValue(expectedResponse);
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест отображения количества незаполненых учеток', async () => {
        
    const wrapper = shallowMount(Main, {
      localVue,
      vuetify,
    });

    await flushPromises();

    expect(mockCount).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.noProfileCount).toBe(expectedCount);
  });

  it('Тест ссылок в панели управления', async () => {
    localVue.use(VueRouter);
    const wrapper = shallowMount(Main, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();
    // FIXME Узнать как тестировать ссылки роутера
  });

  it('Тест вызова окна с ошибкой при ошибке загрузки количества незаполненых учеток', () => {

  });

})