<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо {{ companyInfo.title }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-card>
        <v-card-title>
          Учетная запись
        </v-card-title>
      </v-card>
      </v-col>
      <v-col cols="8">
        <EditCompanyForm v-bind:initial="companyInfo" ref="editCompanyForm"></EditCompanyForm>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import companiesApi from '@/core/services/http/companies';
import EditCompanyForm from '@/core/components/companies/EditCompanyForm';
// import statuses from "@/core/services/statuses";
import eventsUtils from '@/core/services/events/utils';
import { processHttpError } from '@/core/services/errors/utils';

export default {
  data () {
    return {
      companyInfo: {}
    }
  },
  components: {
    EditCompanyForm: EditCompanyForm,
  },
  computed: {
    companyUuid() {
      return this.$route.params.companyUuid;
    }
  },
  mounted() {
    this.getCompanyInfo();
  },
  methods: {
    async getCompanyInfo() {
      let response;
      try {
        response = await companiesApi.detail(this.companyUuid);
      } catch (err) {
        return processHttpError(err);
      }
      if (response.data.uuid == this.companyUuid) {
        this.companyInfo = response.data;
      } else {
        eventsUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о юрлице. Получен ответ ${response}`);
      }
    }
  },
}
</script>