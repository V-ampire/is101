import Vue from 'vue'
import Vuetify from 'vuetify'
import CompanyListTable from '@/core/components/companies/CompanyListTable'

import {
  mount,
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

describe("Тест для компонента CompanyListTable.vue", () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify()
  });

  // it("Тест метода getCompanies()", () => {

  // });

  it("Инициализация компонента с данными от метода getCompanies()", async () => {
    const mockMethod = jest.spyOn(CompanyListTable.methods, 'getCompanies');

    const wrapper = mount(CompanyListTable, {
      localVue,
      vuetify,
    });
    const companiesTable = wrapper.findComponent(CompanyListTable);

    expect(companiesTable.exists()).toBe(true);
    expect(mockMethod.mock.calls.length).toBe(1);

  });
})