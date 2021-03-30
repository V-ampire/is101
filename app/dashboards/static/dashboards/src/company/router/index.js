import Vue from 'vue'
import VueRouter from 'vue-router'
import CompanyDetail from '@/company/views/companies/CompanyDetail.vue'
import BranchDetail from '@/company/views/branches/BranchDetail.vue'
import EmployeeDetail from '@/company/views/employees/EmployeeDetail.vue'
import config from '@/config'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'CompanyDetail',
    component: CompanyDetail,
  },
  {
    path: '/branches/:branchUuid',
    name: 'BranchDetail',
    component: BranchDetail,    
  },
  {
    path: '/branches/:branchUuid/employees/:employeeUuid',
    name: 'EmployeeDetail',
    component: EmployeeDetail,    
  },
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router
