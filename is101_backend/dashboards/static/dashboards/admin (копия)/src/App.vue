<template>
<v-app>
  <div class="snackbars">
    <status-alert></status-alert>
    <confirm-dialog></confirm-dialog>
  </div>
  <v-main>
    <v-container>
      <company-list></company-list>
    </v-container>
  </v-main>
</v-app>
</template>

<script>
import CompanyList from '@/components/companies/CompanyList'
import ConfirmDialog from '@/components/base/ConfirmDialog'
import StatusAlert from '@/components/base/StatusAlert'

export default {
  name: 'App',

  components: {
    'company-list': CompanyList,
    'confirm-dialog': ConfirmDialog,
    'status-alert': StatusAlert
  },

  data: () => ({
    //
  }),
};
</script>
