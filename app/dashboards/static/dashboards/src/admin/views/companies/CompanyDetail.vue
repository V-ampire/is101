<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо {{ companyInfo.title }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <v-card>
        <v-card-title class="subtitle-1">
          Редактировать учетную запись
        </v-card-title>
        <v-card-text>
          <EditAccountForm
            v-if="!!companyInfo.user" 
            :accountUuid="companyInfo.user.uuid" 
            ref="editAccountForm"></EditAccountForm>
        </v-card-text>
      </v-card>
      </v-col>
      <v-col cols="7">
        <EditCompanyForm ref="editCompanyForm"></EditCompanyForm>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import companiesApi from '@/core/services/http/companies';
import EditCompanyForm from '@/core/components/companies/EditCompanyForm';
import EditAccountForm from '@/core/components/accounts/EditAccountForm';
import eventUtils from '@/core/services/events/utils';
import errorUtils from '@/core/services/errors/utils';

export default {
  data () {
    return {
      companyInfo: {}
    }
  },
  components: {
    EditCompanyForm: EditCompanyForm,
    EditAccountForm: EditAccountForm,
  },
  computed: {
    companyUuid() {
      return this.$route.params.companyUuid;
    },
  },
  async mounted() {
    let vm = this;
    this.companyInfo = await this.getCompanyInfo();
    this.$nextTick(() => {
      vm.$refs.editCompanyForm.setInitial(this.companyInfo);
      vm.$refs.editAccountForm.setInitial(this.companyInfo.user);
    });
  },
  methods: {
    async getCompanyInfo() {
      let response;
      try {
        response = await companiesApi.detail(this.companyUuid);
      } catch (err) {
        const httpError = errorUtils.checkHttpError(err);
        eventUtils.showErrorAlert(httpError.message);
        throw err
      }
      if (response.data.uuid == this.companyUuid) {
        return response.data
      } else {
        eventsUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о юрлице. Получен ответ ${response}`);
      }
    }
  },
}
</script>