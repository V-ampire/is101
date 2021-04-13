import Vue from 'vue'
import VueRouter from 'vue-router'
import config from '@/config'

import Profile from '@/company/views/Profile';
import BranchList from '@/company/views/BranchList';
import BranchDetail from '@/company/views/BranchDetail';
import EmployeeDetail from '@/company/views/EmployeeDetail';

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
  },
  {
    path: '/:companyUuid/branches/:branchUuid',
    name: 'BranchDetail',
    component: BranchDetail,    
  },
  {
    path: '/companies/:companyUuid/branches/:branchUuid/employees/:employeeUuid',
    name: 'EmployeeDetail',
    component: EmployeeDetail,    
  },
]

const router = new VueRouter({
  mode: 'history',
  base: config.companyBaseUrl,
  routes
})

export default router
