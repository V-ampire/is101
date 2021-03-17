<template>
  <v-form ref="form">
    <div class="status-info mb-2">
      <h3 class="mb-2">Текущий статус</h3>
      <span v-if="currentStatus=='works'">
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-briefcase</v-icon>
        </v-btn> - В работе
      </span>
      <span v-else>
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-archive</v-icon>
        </v-btn> - В архиве
      </span>
    </div>
    <div class="form-btn">
      <div v-if="currentStatus=='works'" class="form-btn-toWork">
        <v-btn
          color="primary"
          small
          block
          @click="toArchive()"
        >
          <v-icon class="mr-2" small>fa-archive</v-icon> Перевести в архив
        </v-btn>
      </div>
      <div v-else class="form-btn-toArchive">
        <v-btn
          color="primary"
          small
          block
          @click="toWork()"
        >
          <v-icon class="mr-2" small>fa-briefcase</v-icon> Перевести в работу
        </v-btn>
      </div>
    </div>
  </v-form>
</template>

<script>
export default {
  props: {
    currentStatus: String
  },
  methods: {
    toArchive() {
      this.$emit('onToArchive');
    },
    toWork() {
      this.$emit('onToWork');
    }
  },
}
</script>