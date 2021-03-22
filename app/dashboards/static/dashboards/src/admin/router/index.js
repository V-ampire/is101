import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '@/admin/views/Main.vue'
import CompanyList from '@/admin/views/companies/CompanyList.vue'
import CompanyDetail from '@/admin/views/companies/CompanyDetail.vue'
import BranchDetail from '@/admin/views/branches/BranchDetail.vue'
import EmployeeDetail from '@/admin/views/employees/EmployeeDetail.vue'
import config from '@/config'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/companies',
    name: 'CompanyList',
    component: CompanyList,
  },
  {
    path: '/companies/:companyUuid',
    name: 'CompanyDetail',
    component: CompanyDetail,
  },
  {
    path: '/companies/:companyUuid/branches/:branchUuid',
    name: 'BranchDetail',
    component: BranchDetail,    
  },
  {
    path: '/companies/:companyUuid/branches/:branchUuid/employees/:employeeUuid',
    name: 'EmployeeDetail',
    component: EmployeeDetail,    
  }
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router
