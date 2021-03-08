import Vuetify from 'vuetify';
import CompanyDetail from '@/admin/views/companies/CompanyDetail';
import EditAccountForm from '@/core/components/accounts/EditAccountForm';
import companies from '@/core/services/http/companies';
import statuses from "@/core/services/statuses";
import router from '@/admin/router';

import { createLocalVue, mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';
import { CompanyApi } from '../apiFactories';

describe('Тест для отображения страницы редактирования юрлица', () => {

  const expectedCompany = CompanyApi.detail()

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест заголовка', async () => {
    const wrapper = mount(CompanyDetail, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    await wrapper.setData({
      companyInfo: expectedCompany
    });

    const expectedH1 = `Юрлицо ${expectedCompany.title}`;

    expect(wrapper.find('h1').text()).toEqual(expectedH1);
  });

  it('Тест монтирования компонента', async () => {
    // const expectedResponse = {data: expectedCompany}
    // jest.spyOn(companies, 'detail').mockResolvedValue(expectedResponse);
    // const mockCompanyInit = jest.fn();
    // const mockUserInit = jest.fn();
    // const components = {
    //   EditCompanyForm: {setInitial: mockCompanyInit},
    //   EditAccountForm: {setInitial: mockUserInit},
    // };

    // const wrapper = mount(CompanyDetail, {
    //   localVue,
    //   vuetify,
    //   router,
    //   components
    // });

    // await flushPromises();

    // expect(wrapper.vm.companyInfo).toEqual(expectedCompany);
    // expect(mockCompanyInit).toHaveBeenCalledWith(expectedCompany);
    // expect(mockUserInit).toHaveBeenCalledWith(expectedCompany.user);
  });
})