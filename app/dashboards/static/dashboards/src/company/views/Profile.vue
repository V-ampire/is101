<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо</h1>
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
              <AccountEditForm
                v-if="!!companyInfo.user" 
                :accountUuid="companyInfo.user.uuid"
                :accountRole="accountRole"
                ref="accountEditForm"
                @onReload="reloadData"
              ></AccountEditForm>
              <div class="password-field">
                <v-dialog
                  v-model="passwordDialog"
                  max-width="360"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <div class="password-field-btn">
                      <v-btn
                        color="primary"
                        small
                        block
                        v-bind="attrs"
                        v-on="on"
                      >
                        Изменить пароль
                      </v-btn>
                    </div>
                  </template>
                  <v-card>
                    <v-card-title>Изменить пароль</v-card-title>
                    <v-card-text>
                      <ChangePasswordForm
                        :accountUuid="companyInfo.user.uuid"
                        :accountRole="accountRole"
                        @onReload="reloadData"
                      ></ChangePasswordForm>
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col cols="7">
        <v-card>
          <v-card-title class="subtitle-1">
            Редактировать профиль.
          </v-card-title>
          <v-card-text>
            <EditCompanyForm
              v-if="!!companyInfo"
              :companyUuid="companyUuid"
              ref="editCompanyForm"
              @onReload="reloadData"
            ></EditCompanyForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { companiesApi } from '@/core/services/http/clients';
import config from '@/config';
import roles from '@/core/services/roles';
import eventUtils from '@/core/services/events/utils';

import AccountEditForm from '@/core/components/accounts/AccountEditForm';
import ChangePasswordForm from '@/core/components/accounts/ChangePasswordForm';
import EditCompanyForm from '@/core/components/companies/EditCompanyForm';

export default {
  components: {
    AccountEditForm: AccountEditForm,
    ChangePasswordForm: ChangePasswordForm,
    EditCompanyForm: EditCompanyForm
  },
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
  async mounted() {
    this.companyInfo = await this.getCompanyInfo();
    await this.$nextTick(() => {
      this.$refs.accountEditForm.setInitial(this.companyInfo.user);
      this.$refs.editCompanyForm.setInitial(this.companyInfo);
    });
  },
  methods: {
    async reloadData() {
      this.companyInfo = await this.getCompanyInfo();
      this.$refs.accountEditForm.setInitial(this.companyInfo.user);
      this.$refs.editCompanyForm.setInitial(this.companyInfo);
    },
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
  },
}
</script>

