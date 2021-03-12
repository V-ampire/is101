import { createLocalVue, mount, shallowMount } from '@vue/test-utils';
import router from '@/admin/router';
import VueRouter from 'vue-router'
import Vuetify from 'vuetify';


export function createTestVue () {
  const localVue = createLocalVue();
  localVue.use(VueRouter);
  localVue.use(Vuetify);
};


export function createWrapper (component, options = {}) {
  const localVue = createTestVue();
  const vuetify = new Vuetify();
  return mount(component, {
    router,
    localVue,
    vuetify,
    ...options
  })
};


export function createShallowWrapper (component, options = {}) {
  const localVue = createTestVue();
  const vuetify = new Vuetify();
  return shallowMount(component, {
    localVue,
    vuetify,
    ...options
  })
};