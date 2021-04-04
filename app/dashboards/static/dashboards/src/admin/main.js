import Vue from 'vue'
import App from '@/admin/App.vue'
import router from '@/admin/router'
import vuetify from '@/plugins/vuetify';
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false

Vue.use(VueCookies)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
