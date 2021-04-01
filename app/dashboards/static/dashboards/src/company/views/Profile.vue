<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо {{ companyInfo }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <div class="d-flex flex-column">
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">
              Редактировать учетную запись
            </v-card-title>
            <v-card-text>
              <!-- <AccountEditForm
                v-if="!!companyInfo.user" 
                :accountUuid="companyInfo.user.uuid"
                :accountRole="accountRole"
                ref="accountEditForm"
                @onReload="reloadData"
              ></AccountEditForm> -->
            </v-card-text>
          </v-card>
        </div>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
import { companiesApi } from '@/core/services/http/clients';
import config from '@/config';
import roles from '@/core/services/roles';
import eventUtils from '@/core/services/events/utils';

//import AccountEditForm from '@/core/components/accounts/AccountEditForm';

export default {
  // components: {
  //   AccountEditForm: AccountEditForm
  // },
  data() {
    return {
      companyInfo: null,
      accountRole: roles.company[0]
    }
  },
  computed: {
    companyUuid() {
      return this.$cookies.get(config.profileUuidCookie)
    },
    api() {
      return companiesApi()
    }
  },
  // async mounted() {
  //   console.log('mounted')
  //   // let response;
  //   // response = await this.api.detail(this.companyUuid);
  // },
  methods: {
    async getCompanyInfo() {
      let response;
      try {
        response = await this.api.detail(this.companyUuid);
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (response.data.uuid == this.companyUuid) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о юрлице. Получен ответ ${response}`);
      }
    },
  }
}
</script>

