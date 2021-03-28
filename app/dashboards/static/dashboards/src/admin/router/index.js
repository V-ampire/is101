import Vue from 'vue'
import VueRouter from 'vue-router'
import AccountDetail from '@/admin/views/accounts/AccountDetail.vue'
import CompanyList from '@/admin/views/companies/CompanyList.vue'
import CompanyDetail from '@/admin/views/companies/CompanyDetail.vue'
import BranchDetail from '@/admin/views/branches/BranchDetail.vue'
import EmployeeDetail from '@/admin/views/employees/EmployeeDetail.vue'
import PositionList from '@/admin/views/positions/PositionList.vue'
import config from '@/config'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'AccountDetail',
    component: AccountDetail
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
  },
  {
    path: 'positions',
    name: 'PositionList',
    component: PositionList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router
