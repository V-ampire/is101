import CompanyListTable from '@/core/components/companies/CompanyListTable';
import CompanyList from '@/admin/views/companies/CompanyList';

import Vuetify from 'vuetify';
import faker from 'faker';
import { createLocalVue, shallowMount } from '@vue/test-utils';

describe('Тест для отображения списка юрлиц', () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест привязки пропа search к таблице юрлиц', done => {
    const wrapper = shallowMount(CompanyList, {
      localVue,
      vuetify,
    });

    const expected_search = faker.lorem.word();

    wrapper.setData({search: expected_search});

    wrapper.vm.$nextTick(() => {
      const listTable = wrapper.findComponent(CompanyListTable);
      expect(listTable.props('search')).toBe(expected_search);
      done();
    });
    
  })
})