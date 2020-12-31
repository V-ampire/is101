<template>
<v-app>
  <div class="snackbars">
    <status-snackbar></status-snackbar>
  </div>
  <v-main>
    <v-container>
    </v-container>
  </v-main>
</v-app>
</template>

<script>
import StatusSnackbar from '@/components/snackbars/TheStatusSnackbar'
import {OPEN_STATUS_ALERT} from '@/events/eventsList'
import EventBus from '@/events/eventBus'

export default {
  name: 'App',

  components: {
    'status-snackbar': StatusSnackbar
  },

  data: () => ({
    //
  }),
  mounted() {
    setTimeout(() => {
      console.log('Emititng!');
      EventBus.$emit(OPEN_STATUS_ALERT, {status: 'error', message: 'Error message!'})
    }, 5000)
  },
};
</script>
