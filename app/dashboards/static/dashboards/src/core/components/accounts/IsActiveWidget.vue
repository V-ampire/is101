<template>
  <div class="isActive-field">
    <div class="isActive-field-label subtitle-2">Доступ в систему:</div>
    <div class="isActive-field-switch">
      <v-switch
        v-model="isActive"
        :label="isActive ? 'Доступ разрешен' : 'Доступ ограничен'"
        @change="changeSwitch"
      >
        <template v-slot:label>
          <span v-if="inProgress">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </span>
          <span class="green--text ml-2" v-else-if="isActive">
            <v-icon color="green">fa-check-circle</v-icon> Доступ разрешен
          </span>
          <span class="red--text ml-2" v-else>
            <v-icon color="red">fa-times-circle</v-icon> Доступ ограничен
          </span>
        </template>
      </v-switch>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isActive: Boolean,
    inProgress: {
      type: Boolean,
      default: false
    },
  },
  methods: {
    changeSwitch() {
      this.$emit('change');
    }
  },
}
</script>