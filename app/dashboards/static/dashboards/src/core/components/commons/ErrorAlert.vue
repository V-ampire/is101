<template>
  <v-snackbar 
    v-model="showAlert" 
    :color="white"
    :timeout="timeout"
    light
    top
  >
    <div class="alert-close d-flex justify-end">
      <v-btn text @click="showAlert = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>
    <v-alert dense outlined type="error">
      {{ message }}
    </v-alert>
  </v-snackbar>
</template>


<script>
import { ON_APP_ERROR } from '@/core/events/types'
import eventBus from '@/core/events/eventBus'

export default {
  data () {
    return {
      showAlert: false,
      message: '',
      timeout: 6000
    }
  },
  mounted: function() {
    var self = this;

    eventBus.$on(ON_APP_ERROR, (errorData) => {
      self.open(errorData.message)
    });
  },
  methods: {
    open(message) {
      this.message = message;
      this.showAlert = true;
    }
  },
}
</script>

