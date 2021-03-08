<template>
  <v-form ref="form">
    <div class="status-info mb-2">
      <h3 class="mb-2">Текущий статус</h3>
      <span v-if="companyStatus=='works'">
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-briefcase</v-icon>
        </v-btn> - В работе
      </span>
      <span v-else>
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-archive</v-icon>
        </v-btn> - В архивеs
      </span>
    </div>
    <div class="form-btn">
      <div v-if="companyStatus=='works'" class="form-btn-toWork">
        <v-btn
          color="primary"
          small
          block
          @click="toArchve()"
        >
          <v-icon small>fa-archive</v-icon> Перевести в архив
        </v-btn>
      </div>
      <div v-else class="form-btn-toArchive">
        <v-btn
          color="primary"
          small
          block
        >
          <v-icon small>fa-briefcase</v-icon> Перевести в работув
        </v-btn>
      </div>
    </div>
  </v-form>
</template>

<script>
export default {
  props: {
    companyUuid: String,
    companyStatus: String
  },
  data () {
    return {

    }
  },
  methods: {
    
  },
}
</script>