import Vuetify from 'vuetify'
import accounts from '@/core/services/http/accounts';
import Main from '@/admin/views/Main';
import router from '@/admin/router';


import { createLocalVue, shallowMount, mount } from '@vue/test-utils';
import faker from 'faker';
import flushPromises from 'flush-promises';


describe('Тест для отображения главной страницы админки для админов', () => {

  const localVue = createLocalVue();
  let vuetify;

  const expectedCount = faker.random.number();
  const mockResponse = {data: {count: expectedCount}}
  jest.spyOn(accounts.noProfiles, 'count').mockResolvedValue(mockResponse);

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест отображения количества незаполненых учеток', async () => {
        
    const wrapper = shallowMount(Main, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    expect(wrapper.find('.accounts-alert-btn').text()).toEqual(expectedCount.toString());
  });

  it('Тест для подсказки для незаполненных учеток', async () => {
    const wrapper = shallowMount(Main, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    const tooltip = wrapper.findComponent({name: 'v-tooltip'});

    expect(tooltip.props().activator).toEqual('.accounts-alert-btn');
    expect(wrapper.find('.accounts-alert-note').text()).toEqual(
      `Найдено ${expectedCount} учетных записей с незаполненым профилем!`
    );
  });

  it('Тест ссылки на юрлица в панели управления', async () => {
    const wrapper = mount(Main, {
      localVue,
      vuetify,
      router
    });

    const expectedHref = router.resolve({name: 'CompanyList'}).href

    await flushPromises();
    const companiesLink = wrapper.find('.companies a')

    expect(companiesLink.text()).toEqual('Юридические лица');
    expect(companiesLink.attributes().href).toEqual(expectedHref);
  });

  it('Тест ссылки на незаполненные учетки', async () => {
    const wrapper = mount(Main, {
      localVue,
      vuetify,
      router
    });

    const expectedHref = router.resolve({name: 'NoProfileslist'}).href

    await flushPromises();

    const noProfilesLink = wrapper.find('.accounts-alert a')

    expect(noProfilesLink.text()).toEqual(expectedCount.toString());
    expect(noProfilesLink.attributes().href).toEqual(expectedHref);
  });

})