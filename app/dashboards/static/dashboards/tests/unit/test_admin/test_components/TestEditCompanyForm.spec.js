import EditCompanyForm from '@/core/components/companies/EditCompanyForm';
import companiesApi from '@/core/services/http/companies';
import eventUtils from '@/core/services/events/utils';
import Vuetify from 'vuetify';

import { CompanyApi } from '../apiFactories';
import faker from 'faker';
import { createLocalVue, mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';

describe('Тест формы для редактирвания информации о юрлице', () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  const initialData = CompanyApi.detail();

  it('Тест полей формы', () => {
    const expectedFields = {
      title: { value: '', errors: [] },
      logo: { value: '', errors: [] },
      tagline: { value: '', errors: [] },
      inn: { value: '', errors: [] },
      ogrn: { value: '', errors: [] },
      city: { value: '', errors: [] },
      address: { value: '', errors: [] },
      email: { value: '', errors: [] },
      phone: { value: '', errors: [] },
    }
    const wrapper = mount(EditCompanyForm, {
      localVue,
      vuetify,
      propsData: {
        companyUuid: initialData.uuid
      }
    });

    expect(wrapper.vm.fields).toEqual(expectedFields);

  });

  it('Тест отправки формы', async () => {

    const mockUpdate = jest.spyOn(companiesApi, 'update').mockResolvedValue(1);
    const mockAlert = jest.spyOn(eventUtils, 'showSuccessEvent');
    const expectedTitle = faker.company.companyName();

    const wrapper = mount(EditCompanyForm, {
      localVue,
      vuetify,
      propsData: {
        companyUuid: initialData.uuid
      }
    });

    wrapper.vm.setInitial(initialData);

    await wrapper.vm.$nextTick();

    const expectedFormData = wrapper.vm.getAsFormData();
    expectedFormData.set('title', expectedTitle);

    const titleInput = wrapper.find('.title-field-input input');
    titleInput.element.value = expectedTitle;
    await titleInput.trigger('input');
    
    await wrapper.find('.form-btn button').trigger('click')

    await flushPromises();

    expect(mockUpdate).toHaveBeenCalledWith(initialData.uuid, expectedFormData);
    expect(mockAlert).toHaveBeenCalledWith('Данные изменены!');
  });

  it('Тест отправки формы со строкой вместо файла логотипа', async () => {

    const wrapper = mount(EditCompanyForm, {
      localVue,
      vuetify,
      propsData: {
        companyUuid: initialData.uuid
      }
    });

    wrapper.vm.setInitial(initialData);

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.getAsFormData().has('logo')).toBe(false);
  });
})