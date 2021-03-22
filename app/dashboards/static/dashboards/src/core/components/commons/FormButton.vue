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
    label: String,
    inProgress: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    performAction() {
      this.$emit('onAction');
    }
  },
}
</script>