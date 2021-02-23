<template>
    <v-snackbar
        v-model="showAlert"
        color="error"
        top
    >
        {{ message }}
    </v-snackbar>
</template>

<script>
import utils from '@/core/services/events/utils'

export default {
    data () {
        return {
            showAlert: false,
            message: '',
            timeout: 5000
        }
    },
    mounted: function() {
      utils.onErrorEvent(this.open);
    },
    methods: {
      open (message) {
          this.message = message;
          this.showAlert = true;
      }
    }
}
</script>