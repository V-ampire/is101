import ChangePasswordForm from '@/core/components/accounts/ChangePasswordForm';
import accounts from '@/core/services/http/accounts';
import eventUtils from '@/core/services/events/utils';
import Vuetify from 'vuetify';

import faker from 'faker';
import { generatePassword } from '@/core/services/accounts/utils';
import { createLocalVue, mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';
import { ServerError } from '@/core/services/errors/types';

describe('Тест формы изменения пароля', () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  const expectedAccountUuid = faker.random.uuid();
  const expectedNewPassword = generatePassword();

  it('Тест отправки данных', async () => {
    const mockChange = jest.spyOn(accounts.companies, 'changePassword').mockResolvedValue(1);
    const mockAlert = jest.spyOn(eventUtils, 'showSuccessEvent');

    const expectedFormData = new FormData();
    expectedFormData.append('password1', expectedNewPassword);
    expectedFormData.append('password2', expectedNewPassword);

    const wrapper = mount(ChangePasswordForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccountUuid
      }
    });

    const passwordInput1 = wrapper.find('.password1-field input');
    const passwordInput2 = wrapper.find('.password2-field input');
    passwordInput1.element.value = expectedNewPassword;
    await passwordInput1.trigger('input');
    passwordInput2.element.value = expectedNewPassword;
    await passwordInput2.trigger('input');
    await wrapper.find('.form-btn-change button').trigger('click');

    await flushPromises();

    expect(mockChange).toHaveBeenCalledWith(expectedAccountUuid, expectedFormData);
    expect(mockAlert).toHaveBeenCalledWith('Пароль изменен!');
  });

  it('Тест отображения ошибки поля ', async () => {
    const expectedErrors = [faker.lorem.sentence()];
    const expectedResponse = {
      data: {
        password1: expectedErrors
      }
    }

    jest.spyOn(accounts.companies, 'changePassword')
      .mockRejectedValue(new ServerError({response: expectedResponse}));
    
    const wrapper = mount(ChangePasswordForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: faker.random.uuid()
      }
    });

    const passwordInput1 = wrapper.find('.password1-field input');
    const passwordInput2 = wrapper.find('.password2-field input');
    passwordInput1.element.value = expectedNewPassword;
    await passwordInput1.trigger('input');
    passwordInput2.element.value = expectedNewPassword;
    await passwordInput2.trigger('input');
    await wrapper.find('.form-btn-change button').trigger('click');

    await flushPromises();

    expect(wrapper.vm.fields.password1.errors).toEqual(expectedErrors);
  });

  it('Тест отображения глобальной ошибки', async () => {
    const expectedErrorMessage = faker.lorem.sentence();

    const mockAlert = jest.spyOn(eventUtils, 'showErrorAlert');

    jest.spyOn(accounts.companies, 'changePassword')
      .mockRejectedValue(new Error(expectedErrorMessage));

    const wrapper = mount(ChangePasswordForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: faker.random.uuid()
      }
    });

    const passwordInput1 = wrapper.find('.password1-field input');
    const passwordInput2 = wrapper.find('.password2-field input');
    passwordInput1.element.value = expectedNewPassword;
    await passwordInput1.trigger('input');
    passwordInput2.element.value = expectedNewPassword;
    await passwordInput2.trigger('input');
    await wrapper.find('.form-btn-change button').trigger('click');

    await flushPromises();

    expect(mockAlert).toHaveBeenCalledWith(expectedErrorMessage);
  });
})