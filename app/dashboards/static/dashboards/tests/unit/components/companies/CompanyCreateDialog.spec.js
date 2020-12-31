import Vue from 'vue'
import Vuetify from 'vuetify'
import CreateCompanyDialog from '@/core/components/companies/CreateCompanyDialog'

import {
  mount,
  createLocalVue
} from '@vue/test-utils'
Vue.use(Vuetify);


describe("Тест для компонента CreateCompanyDialog.vue", () => {
  const localVue = createLocalVue();
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify()
  });

  it("Тест инициализации компонента", () => {
    const wrapper = mount(CreateCompanyDialog, {
      localVue,
      vuetify,
    });
    const dialog = wrapper.findComponent(CreateCompanyDialog);

    expect(dialog.exists()).toBe(true);
  });

  it("Тест метода onError(error) c серверной ошибкой 400 (не валидные данные)", () => {
    const mockMethod = jest.spyOn(CreateCompanyDialog.methods, 'setComponentError');

    const wrapper = mount(CreateCompanyDialog, {
      localVue,
      vuetify,
    });

    const error = {
      response: {
        status: 400
      }
    };

    wrapper.vm.onError(error);

    expect(mockMethod.mock.calls.length).toBe(1);
    expect(mockMethod.mock.calls[0] == [error])
  });

  // it("Тест вызова функции processHttpError в методе onError(error) ", () => {
  //   //const mockFunction = jest.doMock('@/core/services/http/utils.js');

  //   const mockFn = jest.fn();
  //   utils.processHttpError = mockFn

  //   const wrapper = mount(CreateCompanyDialog, {
  //     localVue,
  //     vuetify,
  //   });

  //   const error = {
  //     response: {
  //       status: 404
  //     }
  //   };

  //   wrapper.vm.onError(error);

  //   expect(mockFunction.mock.calls.length).toBe(1);
  //   expect(mockFunction.mock.calls[0] == [error])
  // })
})