<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-card>
          <v-card-title class="subtitle-1">Редактировать учетную запись</v-card-title>
          <v-card-text>
            <AccountEditForm
              ref="accountEditForm" 
              v-if="!!accountInfo"
              :accountUuid="accountUuid"
              :accountRole="accountRole"
            ></AccountEditForm>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6">
        <v-card>
          <v-card-title class="subtitle-1">Изменить пароль</v-card-title>
          <v-card-text>
            <ChangePasswordForm
              :accountUuid="accountUuid"
              :accountRole="accountRole"
            ></ChangePasswordForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import AccountEditForm from '@/core/components/accounts/AccountEditForm';
import ChangePasswordForm from '@/core/components/accounts/ChangePasswordForm';
import config from '@/config';
import roles from '@/core/services/roles';
import { adminAccountsApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';

export default {
  components: {
    AccountEditForm: AccountEditForm,
    ChangePasswordForm: ChangePasswordForm
  },
  data() {
    return {
      accountRole: roles.admin[0],
      accountInfo: null
    }
  },
  computed: {
    accountUuid() {
      return this.$cookies.get(config.userUuidCookie)
    },
  },
  async mounted() {
    this.accountInfo = await this.getAccountInfo();
    await this.$nextTick(() => {
      this.$refs.accountEditForm.setInitial(this.accountInfo);
    });
  },
  methods: {
    async getAccountInfo() {
      let response;
      try {
        response = await adminAccountsApi().detail(this.accountUuid);
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (response.data.uuid == this.accountUuid) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию об учетной записи. Получен ответ ${response}`);
      }
    }
  },
}
</script>