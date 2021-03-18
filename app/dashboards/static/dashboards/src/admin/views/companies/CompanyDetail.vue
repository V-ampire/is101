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
                @onReload="reloadData()"
                ref="editCompanyStatusForm"></EditCompanyStatusForm>
            </v-card-text>
          </v-card>
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">Филиалы юрлица</v-card-title>
            <v-card-text>
              <BranchListTable
                v-if="!!companyInfo.branches"
                :branchList="companyInfo.branches"
                ref="branchListTable"
                @onReload="reloadData()"
              ></BranchListTable>
            </v-card-text>
            <v-card-actions>
              <v-dialog
                v-model="dialog"
                max-width="600px"
                @click:outside="resetBranchCreateForm()"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                    small
                    block
                  >
                    Добавить филиал
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="subtitle-1">Добавить новый филиал</v-card-title>
                  <v-card-text>
                    <BranchCreateForm
                      :companyUuid="companyUuid"
                      ref="branchCreateForm"
                      @onReload="reloadData()"
                    ></BranchCreateForm>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-card-actions>
          </v-card>
          <v-card>
            <v-card-title class="subtitle-1">Удалить юрлицо</v-card-title>
            <v-card-subtitle class="body-2 text-wrap-normal">
              При удалении юрлица одновременно будет удалена вся информация 
              о филиалах и работниках юрлица. Также будет удалена его учетная запись.
            </v-card-subtitle>
            <v-card-text>
              <v-btn 
                color="error"
                small
                block
                @click="deleteCompany()"
              >
                Удалить юрлицо
              </v-btn>
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
import {companiesApi} from '@/core/services/http/clients';
import EditCompanyForm from '@/core/components/companies/EditCompanyForm';
import EditCompanyStatusForm from '@/core/components/companies/EditCompanyStatusForm';
import EditAccountForm from '@/core/components/accounts/EditAccountForm';
import BranchListTable from '@/core/components/branches/BranchListTable';
import BranchCreateForm from '@/core/components/branches/BranchCreateForm';
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
    BranchListTable: BranchListTable,
    BranchCreateForm: BranchCreateForm
  },
  computed: {
    companyUuid() {
      return this.$route.params.companyUuid;
    },
    api() {
      return companiesApi()
    }
  },
  async mounted() {
    this.companyInfo = await this.getCompanyInfo();
    await this.$nextTick(() => {
      this.$refs.editAccountForm.setInitial(this.companyInfo.user);
      this.$refs.editCompanyForm.setInitial(this.companyInfo);
    });
  },
  methods: {
    async reloadData() {
      this.companyInfo = await this.getCompanyInfo();
      this.$refs.editAccountForm.setInitial(this.companyInfo.user);
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
    async deleteCompany() {
      const confirmParams = {
        message: `Вы действительно хотите удалить юрлицо ${this.companyInfo.title}`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(this.companyUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо удалено!');
          this.$router.push({name: 'CompanyList'});
        }
      });
    },
    resetBranchCreateForm() {
      this.$refs.resetBranchCreateForm.reset()
    }
  },
}
</script>