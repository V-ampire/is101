import Vue from 'vue'
import VueRouter from 'vue-router'
import config from '@/config'

import Profile from '@/company/views/Profile';
import BranchList from '@/company/views/BranchList';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/branches',
    name: 'BranchList',
    component: BranchList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: config.companyBaseUrl,
  routes
})

export default router
