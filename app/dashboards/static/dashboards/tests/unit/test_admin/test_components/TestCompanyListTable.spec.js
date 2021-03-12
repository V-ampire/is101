import Vuetify from 'vuetify';
import CompanyListTable from '@/core/components/companies/CompanyListTable';
import companies from '@/core/services/http/companies';
import statuses from "@/core/services/statuses";
import router from '@/admin/router';

import { createLocalVue, mount, shallowMount } from '@vue/test-utils';
import { CompanyApi } from '../apiFactories';
import flushPromises from 'flush-promises';
import faker from 'faker';

describe('Тест CompanyListTable.vue', () => {

  const expectedCompaniesList = CompanyApi.list(5);

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест загрузки списка  юрлиц', async () => {
    const expectedResponse = {data: expectedCompaniesList}
    const mockList = jest.spyOn(companies, 'list')
                        .mockResolvedValue(expectedResponse);

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    expect(wrapper.vm.companiesList).toEqual(expectedCompaniesList);
    // expect(wrapper.vm.statuses).toEqual(statuses);
    // expect(wrapper.vm.headers).toEqual(expectedHeaders);
  });

  it('Тест привязки параметров к таблице vuetify', async () => {
    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    const expectedHeaders = [
      {text: 'Название юр. лица', value: 'title'},
      {text: 'Город', value: 'city' },
      {text: 'Адрес', value: 'address' },
      {text: 'Статус', value: 'status' },
      {text: 'Действия', value: 'actions', sortable: false}
    ];
    const expectedSearch = faker.lorem.word();

    wrapper.setData({
      companiesList: expectedCompaniesList, 
      headers: expectedHeaders,
      statuses: statuses
    });

    wrapper.setProps({search: expectedSearch});

    const dataTable = wrapper.findComponent({name: 'v-data-table'});

    expect(dataTable.props().headers).toEqual(wrapper.vm.headers);
    expect(dataTable.props().items).toEqual(wrapper.vm.companiesList);
    expect(dataTable.props().search).toEqual(wrapper.props.search);
  });

  it('Тест клика по кнопку удаления юрлица', async done => {

    const expectedCompany = CompanyApi.list(1)[0];
    expectedCompany.status = statuses.works;

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    const mockDelete = jest.spyOn(wrapper.vm, 'deleteCompany');
    
    await wrapper.setData({
      companiesList: [expectedCompany]
    });

    await wrapper.find('.delete-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockDelete).toHaveBeenCalledTimes(1);
      expect(mockDelete).toHaveBeenCalledWith(expectedCompany);
      done();
    });
  });

  it('Тест клика на кнопку архивирования юрлица', async done => {
    const expectedCompany = CompanyApi.list(1)[0];
    expectedCompany.status = statuses.works;

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    const mockArchive = jest.spyOn(wrapper.vm, 'toAchiveCompany');
    
    await wrapper.setData({
      companiesList: [expectedCompany]
    });

    await wrapper.find('.status-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockArchive).toHaveBeenCalledTimes(1);
      expect(mockArchive).toHaveBeenCalledWith(expectedCompany);
      done();
    });
  });

  it('Тест клика на кнопку деархивирования юрлица', async done => {
    const expectedCompany = CompanyApi.list(1)[0];
    expectedCompany.status = statuses.archived;

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    const mockToWork = jest.spyOn(wrapper.vm, 'toWorkCompany');
    
    await wrapper.setData({
      companiesList: [expectedCompany]
    });

    await wrapper.find('.status-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockToWork).toHaveBeenCalledTimes(1);
      expect(mockToWork).toHaveBeenCalledWith(expectedCompany);
      done();
    });
  });

  it('Тест сслыки на подробную информацию о юрлице', async () => {
    const expectedCompany = CompanyApi.list(1)[0];
    expectedCompany.status = statuses.archived;

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
      router
    });

    await flushPromises();

    await wrapper.setData({
      companiesList: [expectedCompany]
    });

    const expectedHref = router.resolve({
      name: 'CompanyDetail',
      params: {companyUuid: expectedCompany.uuid}
    }).href;

    const companyDetailLink = wrapper.find('.detail-link a');

    expect(companyDetailLink.text()).toEqual(expectedCompany.title);
    expect(companyDetailLink.attributes().href).toEqual(expectedHref);

  })
})




  // it('Тест вызова окна с ошибкой при неожиданном ответе сервера', done => {
  //   const resp = {data: 'Unexpected response.'};

  //   utils.showErrorAlert = jest.fn();
  //   companies.list = jest.fn().mockResolvedValue(resp);

  //   const expectedMessage = 'Не удалось загрузить данные с сервера.';

  //   const wrapper = shallowMount(CompanyListTable, {
  //     localVue,
  //     vuetify,
  //   });

  //   setTimeout(() => {
  //     expect(utils.showErrorAlert).toHaveBeenCalledTimes(1);
  //     expect(utils.showErrorAlert).toHaveBeenCalledWith(expectedMessage);
  //     done();  
  //   }, 2000);
    
  // });

  // it('Тест вызова метода getCompanies при монтировании', () => {
  //   companies.list = jest.fn();

  //   const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies').mockResolvedValue(1);

  //   const wrapper = shallowMount(CompanyListTable, {
  //     localVue,
  //     vuetify,
  //   });

  //   expect(mockMethod).toHaveBeenCalledTimes(1);
  // });

  // it('Тест items', () => {
  //   const companiesList = [{
  //     address: 'testTilte',
  //     city: 'city',
  //     status: 'works',
  //     title: 'testTilte',
  //     url: 'testUrl',
  //     uuid: 'testUuid'
  //   }];

  //   const companyData = companiesList[0];

  //   const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies').mockResolvedValue(1);

  //   const wrapper = shallowMount(CompanyListTable, {
  //     localVue,
  //     vuetify,
  //   });

  //   wrapper.setData({companiesList: companiesList})

  //   const expectedItems = [{
  //     address: companyData.address,
  //     city: companyData.city,
  //     status: statuses[companyData.status],
  //     title: companyData.title,
  //     url: companyData.url,
  //     uuid: companyData.uuid
  //   }];

  //   expect(wrapper.vm.items).toEqual(expectedItems);

  // });
