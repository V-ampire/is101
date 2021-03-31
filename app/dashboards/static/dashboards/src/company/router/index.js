import Vue from 'vue'
import VueRouter from 'vue-router'
import config from '@/config'

import Profile from '@/company/views/Profile';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Profile',
    component: Profile
  },
]

const router = new VueRouter({
  mode: 'history',
  base: config.companyBaseUrl,
  routes
})

export default router
