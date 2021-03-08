import EditAccountForm from '@/core/components/accounts/EditAccountForm';
import Vuetify from 'vuetify';
import accounts from '@/core/services/http/accounts';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';

import { AccountsApi } from '../apiFactories';
import { createLocalVue, mount } from '@vue/test-utils';
import flushPromises from 'flush-promises';
import faker from 'faker';


describe('Тест формы для изменения учетных записей', () => {

  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Тест закрытия доступа', async () => {
    const expectedAccount = AccountsApi.companies.detail();
    expectedAccount.is_active = true;

    const mockDeactivate = jest.spyOn(accounts.companies, 'deactivate').mockResolvedValue(1);
  
    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    wrapper.vm.setInitial(expectedAccount);

    await wrapper.vm.$nextTick();

    wrapper.find('.isActive-field-switch input').trigger('change');

    await flushPromises();

    expect(mockDeactivate).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.fields.is_active.value).toBe(false);
  });

  it('Тест открытия доступа', async () => {
    const expectedAccount = AccountsApi.companies.detail();
    expectedAccount.is_active = false;

    const mockActivate = jest.spyOn(accounts.companies, 'activate').mockResolvedValue(1);
  
    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    wrapper.vm.setInitial(expectedAccount);

    await wrapper.vm.$nextTick();

    wrapper.find('.isActive-field-switch input').trigger('change');

    await flushPromises();

    expect(mockActivate).toHaveBeenCalledTimes(1);
    expect(wrapper.vm.fields.is_active.value).toBe(true);
  });

  it('Тест изменения username', async () => {
    const expectedAccount = AccountsApi.companies.detail();

    const mockUpdate = jest.spyOn(accounts.companies, 'update').mockResolvedValue(1);
    const mockAlert = jest.spyOn(eventUtils, 'showSuccessEvent');

    const expectedUsername = faker.internet.userName()
    const expectedFormData = new FormData();
    expectedFormData.append('username', expectedUsername)
  
    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    wrapper.vm.setInitial(expectedAccount);

    await wrapper.vm.$nextTick();

    const textInput = wrapper.find('.username-field-input input');
    textInput.element.value = expectedUsername;
    await textInput.trigger('input');
    await wrapper.find('.username-field-btn button').trigger('click')

    await flushPromises();
    await wrapper.vm.$nextTick();

    expect(mockUpdate).toHaveBeenCalledWith(expectedAccount.uuid, expectedFormData);
    expect(mockAlert).toHaveBeenCalledWith('Логин обновлен!');
  });

  it('Тест вызова диалога изменения пароля', async () => {
    const expectedAccount = AccountsApi.companies.detail();
    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    await wrapper.find('.password-field-btn button').trigger('click');

    expect(wrapper.vm.passwordDialog).toBe(true);
  });

  it('Тест отображения ошибок поля username', async () => {
    const expectedAccount = AccountsApi.companies.detail();
    const expectedErrors = [faker.lorem.sentence()];
    const expectedResponse = {
      data: {
        username: expectedErrors
      }
    }

    jest.spyOn(accounts.companies, 'update')
      .mockRejectedValue(new ServerError({response: expectedResponse}));

    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    wrapper.vm.setInitial(expectedAccount);

    await wrapper.vm.$nextTick();

    const textInput = wrapper.find('.username-field-input input');
    textInput.element.value = faker.lorem.word(10);
    await textInput.trigger('input');
    await wrapper.find('.username-field-btn button').trigger('click');

    await flushPromises();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.fields.username.errors).toEqual(expectedErrors);
  });

  it('Тест отображения ошибки глобально', async () => {
    const expectedErrorMessage = faker.lorem.sentence();
    const expectedAccount = AccountsApi.companies.detail();

    const mockAlert = jest.spyOn(eventUtils, 'showErrorAlert');

    jest.spyOn(accounts.companies, 'update')
      .mockRejectedValue(new Error(expectedErrorMessage));

    const wrapper = mount(EditAccountForm, {
      localVue,
      vuetify,
      propsData: {
        accountUuid: expectedAccount.uuid
      }
    });

    wrapper.vm.setInitial(expectedAccount);

    await wrapper.vm.$nextTick();

    const textInput = wrapper.find('.username-field-input input');
    textInput.element.value = faker.lorem.word(10);
    await textInput.trigger('input');
    await wrapper.find('.username-field-btn button').trigger('click');

    await flushPromises();

    expect(mockAlert).toHaveBeenCalledWith(expectedErrorMessage);
  });
})