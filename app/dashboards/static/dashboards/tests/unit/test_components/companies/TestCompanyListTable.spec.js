import Vuetify from 'vuetify';
import CompanyListTable from '@/core/components/companies/CompanyListTable';
import companies from '@/core/services/http/companies';
import statuses from "@/core/services/statuses";

import { createLocalVue, mount } from '@vue/test-utils';
import { CompanyListData, CompanyDataForList } from '@/core/factories';
import flushPromises from 'flush-promises';

describe('Тест CompanyListTable.vue', () => {

  const expectedCompaniesList = CompanyListData(5);

  const expectedHeaders = [
    {text: 'Название юр. лица', value: 'title'},
    {text: 'Город', value: 'city' },
    {text: 'Адрес', value: 'address' },
    {text: 'Статус', value: 'status' },
    {text: 'Действия', value: 'actions', sortable: false}
  ];
  
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
    });

    await flushPromises();

    expect(mockList).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.companiesList).toEqual(expectedCompaniesList);
    expect(wrapper.vm.statuses).toEqual(statuses);
    expect(wrapper.vm.headers).toEqual(expectedHeaders);
  });

  it('Тест клика по кнопку удаления юрлица', async done => {

    const expectedList = [CompanyDataForList({status: statuses.works})];

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
    });

    const mockDelete = jest.spyOn(wrapper.vm, 'deleteCompany');
    
    await wrapper.setData({
      companiesList: expectedList
    });

    const expectedItem = wrapper.vm.items[0]

    await wrapper.find('.delete-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockDelete).toHaveBeenCalledTimes(1);
      expect(mockDelete).toHaveBeenCalledWith(expectedItem);
      done();
    });
  });

  it('Тест клика на кнопку архивирования юрлица', async done => {
    const expectedList = [CompanyDataForList({status: statuses.works})];

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
    });

    const mockArchive = jest.spyOn(wrapper.vm, 'toAchiveCompany');
    
    await wrapper.setData({
      companiesList: expectedList
    });

    const expectedItem = wrapper.vm.items[0]

    await wrapper.find('.status-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockArchive).toHaveBeenCalledTimes(1);
      expect(mockArchive).toHaveBeenCalledWith(expectedItem);
      done();
    });
  });

  it('Тест клика на кнопку деархивирования юрлица', async done => {
    const expectedList = [CompanyDataForList({status: statuses.archived})];

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
    });

    const mockToWork = jest.spyOn(wrapper.vm, 'toWorkCompany');
    
    await wrapper.setData({
      companiesList: expectedList
    });

    const expectedItem = wrapper.vm.items[0]

    await wrapper.find('.status-btn button').trigger('click');

    wrapper.vm.$nextTick(() => {
      expect(mockToWork).toHaveBeenCalledTimes(1);
      expect(mockToWork).toHaveBeenCalledWith(expectedItem);
      done();
    });
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
