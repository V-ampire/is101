<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">Юрлицо {{ companyInfo.title }}</h1>
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
              <EditAccountForm
                v-if="!!companyInfo.user" 
                :accountUuid="companyInfo.user.uuid" 
                ref="editAccountForm"></EditAccountForm>
            </v-card-text>
          </v-card>
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">
              Статус юрлица
            </v-card-title>
            <v-card-text>
              <EditCompanyStatusForm
                v-if="!!companyInfo.status" 
                :companyUuid="companyUuid"
                :companyStatus="companyInfo.status"
                ref="editCompanyStatusForm"></EditCompanyStatusForm>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-title class="subtitle-1">Филиалы юрлица</v-card-title>
            <v-card-text>
              <BranchListTable
                v-if="!!companyInfo.branches"
                :branchList="companyInfo.branches"
                ref="branchListTable"
              ></BranchListTable>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col cols="7">
        <v-card>
          <v-card-title class="subtitle-1">
            Редактировать информацию о юрлице.
          </v-card-title>
          <v-card-text>
            <EditCompanyForm
              v-if="!!companyInfo"
              :companyUuid="companyUuid"
              ref="editCompanyForm"
            ></EditCompanyForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import companiesApi from '@/core/services/http/companies';
import EditCompanyForm from '@/core/components/companies/EditCompanyForm';
import EditCompanyStatusForm from '@/core/components/companies/EditCompanyStatusForm';
import EditAccountForm from '@/core/components/accounts/EditAccountForm';
import BranchListTable from '@/core/components/branches/BranchListTable';
import eventUtils from '@/core/services/events/utils';

export default {
  data () {
    return {
      companyInfo: null,
    }
  },
  components: {
    EditCompanyForm: EditCompanyForm,
    EditAccountForm: EditAccountForm,
    EditCompanyStatusForm: EditCompanyStatusForm,
    BranchListTable: BranchListTable
  },
  computed: {
    companyUuid() {
      return this.$route.params.companyUuid;
    },
  },
  async mounted() {
    this.companyInfo = await this.getCompanyInfo();
    await this.$nextTick(() => {
      this.$refs.editAccountForm.setInitial(this.companyInfo.user);
      this.$refs.editCompanyForm.setInitial(this.companyInfo);
    });
    eventUtils.onReloadEvent(async () => {
      this.companyInfo = await this.getCompanyInfo();
      this.$refs.editAccountForm.setInitial(this.companyInfo.user);
      this.$refs.editCompanyForm.setInitial(this.companyInfo);
    })
  },
  methods: {
    async getCompanyInfo() {
      let response;
      try {
        response = await companiesApi.detail(this.companyUuid);
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
    }
  },
}
</script>