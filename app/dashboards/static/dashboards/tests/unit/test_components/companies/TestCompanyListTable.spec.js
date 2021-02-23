import Vuetify from 'vuetify';
import CompanyListTable from '@/core/components/companies/CompanyListTable';
import utils from '@/core/services/events/utils';
import companies from '@/core/services/http/companies';
import statuses from "@/core/services/statuses";

import { createLocalVue, shallowMount } from '@vue/test-utils';

describe('Тест CompanyListTable.vue', () => {

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест вызова окна с ошибкой при неожиданном ответе сервера', done => {
    const resp = {data: 'Unexpected response.'};

    utils.showErrorAlert = jest.fn();
    companies.list = jest.fn().mockResolvedValue(resp);

    const expectedMessage = 'Не удалось загрузить данные с сервера.';

    const wrapper = shallowMount(CompanyListTable, {
      localVue,
      vuetify,
    });

    setTimeout(() => {
      expect(utils.showErrorAlert).toHaveBeenCalledTimes(1);
      expect(utils.showErrorAlert).toHaveBeenCalledWith(expectedMessage);
      done();  
    }, 2000);
    
  });

  it('Тест вызова метода getCompanies при монтировании', () => {
    companies.list = jest.fn();

    const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies').mockResolvedValue(1);

    const wrapper = shallowMount(CompanyListTable, {
      localVue,
      vuetify,
    });

    expect(mockMethod).toHaveBeenCalledTimes(1);
  });

  it('Тест items', () => {
    const companiesList = [{
      address: 'testTilte',
      city: 'city',
      status: 'works',
      title: 'testTilte',
      url: 'testUrl',
      uuid: 'testUuid'
    }];

    const companyData = companiesList[0];

    const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies').mockResolvedValue(1);

    const wrapper = shallowMount(CompanyListTable, {
      localVue,
      vuetify,
    });

    wrapper.setData({companiesList: companiesList})

    const expectedItems = [{
      address: companyData.address,
      city: companyData.city,
      status: statuses[companyData.status],
      title: companyData.title,
      url: companyData.url,
      uuid: companyData.uuid
    }];

    expect(wrapper.vm.items).toEqual(expectedItems);

  });

})