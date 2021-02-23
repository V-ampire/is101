import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '@/admin/views/Main.vue'
import NoProfileslist from '@/admin/views/accounts/NoProfilesList.vue'
import CompanyList from '@/admin/views/companies/CompanyList.vue'
import config from '@/config'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/no_profiles',
    name: 'NoProfileslist',
    component: NoProfileslist
  },
  {
    path: '/companies',
    name: 'CompanyList',
    component: CompanyList
  }
]

const router = new VueRouter({
  mode: 'history',
  base: config.baseUrl,
  routes
})

export default router
