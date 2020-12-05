import Vue from 'vue'
import Vuetify from 'vuetify'
import CompanyListTable from '@/components/companies/CompanyListTable'

import {
  shallowMount,
  createLocalVue
} from '@vue/test-utils'
Vue.use(Vuetify);


var faker = require('faker');

const fakeCompanies = [
  {
    uuid: faker.random.uuid(),
    title: faker.company.companyName(),
    city: faker.address.city(),
    address: faker.address.streetAddress(),
    status: 1,
  },
  {
    uuid: faker.random.uuid(),
    title: faker.company.companyName(),
    city: faker.address.city(),
    address: faker.address.streetAddress(),
    status: 0,
  }
]

jest.doMock('@/services/http/companies', () => {
  return {
    getAll: () => Promise.resolve(fakeCompanies)
  }
});

const localVue = createLocalVue();

describe("Тест для компонента CompanyListTable.vue", () => {
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify()
  });

  // it("Тест метода getCompanies()", () => {

  // });

  it("Инициализация компонента с данными от метода getCompanies()", () => {
    // const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies');
    const wrapper = shallowMount(CompanyListTable, {
      localVue,
      vuetify,
    });
    const companiesTable = wrapper.findComponent(CompanyListTable);

    expect(companiesTable.exists()).toBe(true)
    //expect(companiesTable.vm.companies).toBe(fakeCompanies);

  });
})