import Vuetify from 'vuetify';
import CompanyDetail from '@/admin/views/companies/CompanyDetail';
import companies from '@/core/services/http/companies';
import statuses from "@/core/services/statuses";

import { createLocalVue, mount } from '@vue/test-utils';
import { CompanyDetailData } from '@/core/factories';
import flushPromises from 'flush-promises';

describe('Тест для отображения страницы редактирования юрлица', () => {

  const expectedCompany = CompanyDetailData()

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест заголовка', async () => {
    const wrapper = mount(CompanyDetail, {
      localVue,
      vuetify,
    });

    await wrapper.setData({
      companyInfo: expectedCompany
    });

    await flushPromises();

    const expectedH1 = `Юрлицо ${expectedCompany.title}`;

    expect(wrapper.find('h1').text()).toEqual(expectedH1);
  })
})