<template>
  <v-app>
    <div class="modals">
      <ErrorAlert ref="errorAlert"></ErrorAlert>
      <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    </div>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import ErrorAlert from '@/core/components/commons/ErrorAlert'
import ConfirmDialog from '@/core/components/commons/ConfirmDialog'

export default {
  name: 'App',

  data: () => ({
    //
  }),

  components: {
    'ErrorAlert': ErrorAlert,
    'ConfirmDialog': ConfirmDialog
  },
};
</script>
