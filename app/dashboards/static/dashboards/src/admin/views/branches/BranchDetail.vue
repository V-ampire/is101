<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо {{ branchInfo.title }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <div class="d-flex flex-column">
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">Статус филиала</v-card-title>
            <v-card-text>

            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col cols="7"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import branchesApi from '@/core/services/http/branches';
import eventUtils from '@/core/services/events/utils';

export default {
  data() {
    return {
      branchInfo: null,
    }
  },
  async mounted() {
    this.branchInfo = await this.getBranchInfo();
  },
  computed: {
    branchUuid() {
      return this.$route.params.branchUuid;
    },
    companyUuid() {
      return this.$route.params.companyUuid;
    },
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  methods: {
    async getBranchInfo() {
      let response;
      try {
        response = await this.api.detail(this.branchUuid);
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (response.data.uuid == this.branchUuid) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о филиале. Получен ответ ${response}`);
      }

    }
  },
}
</script>