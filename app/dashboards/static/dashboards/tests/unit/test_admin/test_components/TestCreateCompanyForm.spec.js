import CreateCompanyForm from '@/core/components/companies/CreateCompanyForm';
import companiesApi from '@/core/services/http/companies';
import eventUtils from '@/core/services/events/utils';
import Vuetify from 'vuetify';
import router from '@/admin/router';

import { CompanyApi } from '../apiFactories';
import faker from 'faker';
import { createLocalVue, mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';


async function configure(expectedCompany, localvue, vuetify, options={}) {
  /**
   * Заполнить поля формы.
   * Вернуть заполненный wrapper и formData
   */
  const wrapper = mount(CreateCompanyForm, {
    localvue,
    vuetify,
    ...options
  });

  const usernameInput = wrapper.find('.username-field-input input');
  usernameInput.element.value = expectedCompany.user.username;
  await usernameInput.trigger('input');

  const passwordInput = wrapper.find('.password-field-input input');
  passwordInput.element.value = faker.internet.password();
  await passwordInput.trigger('input');

  const titleInput = wrapper.find('.title-field-input input');
  titleInput.element.value = expectedCompany.title;
  await titleInput.trigger('input');

  // FIXME: Подставить лого в file-input

  const taglineInput = wrapper.find('.tagline-field-input input');
  taglineInput.element.value = expectedCompany.tagline;
  await taglineInput.trigger('input');

  const innInput = wrapper.find('.inn-field-input input');
  innInput.element.value = expectedCompany.inn;
  await innInput.trigger('input');

  const ogrnInput = wrapper.find('.ogrn-field-input input');
  ogrnInput.element.value = expectedCompany.ogrn;
  await ogrnInput.trigger('input');

  const cityInput = wrapper.find('.city-field-input input');
  cityInput.element.value = expectedCompany.city;
  await cityInput.trigger('input');

  const addressInput = wrapper.find('.address-field-input input');
  addressInput.element.value = expectedCompany.address;
  await addressInput.trigger('input');

  const emailInput = wrapper.find('.email-field-input input');
  emailInput.element.value = expectedCompany.email;
  await emailInput.trigger('input');

  const phoneInput = wrapper.find('.phone-field-input input');
  phoneInput.element.value = expectedCompany.phone;
  await phoneInput.trigger('input');

  const formData = wrapper.vm.getAsFormData();

  console.log(formData)

  return { wrapper: wrapper, formData: formData }
};


describe('Тест формы создания нового юрлица', () => {
  const localVue = createLocalVue();
  let vuetify;

  const expectedCompany = CompanyApi.create();

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест успешного создания', async () => {
    const mockCreate = jest.spyOn(companiesApi, 'create').mockResolvedValue(
      {data: expectedCompany}
    );
    const mockReload = jest.spyOn(eventUtils, 'reloadData');

    const { wrapper, expectedFormData } = await configure(expectedCompany, 
      localVue, vuetify, {router: router});

    console.log(expectedFormData)

    const mockValidate = jest.spyOn(wrapper.vm, 'validate').mockReturnValue(true);

    await wrapper.find('.form-btn button').trigger('click')
    await flushPromises();

    // expect(mockCreate).toHaveBeenCalledWith(expectedFormData);
    // expect(mockReload).toHaveBeenCalledTimes(1);
    // expect(mockValidate).toHaveBeenCalledTimes(1);
  });

  it('Тест отображения ошибки при создании', () => {

  });

  it('Тест отображения ссылки на новое юрлицо', () => {

  });

  it('Тест очистки полей формы после создания', () => {

  })
})

