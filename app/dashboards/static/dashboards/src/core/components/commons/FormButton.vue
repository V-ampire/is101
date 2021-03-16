<template>
  <div>
    <v-btn
      small
      block
      :disabled="inProgress"
      color="primary" 
      @click="performAction()"
    >
      {{ label }}
    </v-btn>
    <v-progress-linear
      v-if="inProgress"
      indeterminate
    ></v-progress-linear>
  </div>
</template>

<script>
export default {
  props: {
    label: String
  },
  data () {
    return {
      inProgress: false,
    }
  },
  methods: {
    performAction() {
      try {
        this.inProgress = true;
        this.$emit('onAction');
      } finally {
        this.inProgress = false;
      }
    }
  },
}
</script>