<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="title">Филиал юрлица {{ branchInfo.company }}</h1>
        <h2 class="subtitle-2">
          Адрес филила: {{ branchInfo.city }}, {{ branchInfo.address }}
        </h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <div class="d-flex flex-column">
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">Статус филиала</v-card-title>
            <v-card-text>
              <BranchStatusForm
                v-if="!!branchInfo.status" 
                :branchStatus="branchInfo.status"
                :branchUuid="branchUuid"
                :companyUuid="companyUuid"
                @onReload="reloadData()"
              ></BranchStatusForm>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-title class="subtitle-1">Удалить филиал</v-card-title>
            <v-card-subtitle class="body-2 text-wrap-normal">
              При удалении филиала одновременно будет удалена вся информация о работниках этого филиала.
            </v-card-subtitle>
            <v-card-text>
              <v-btn 
                color="error"
                small
                block
                @click="deleteBranch()"
              >
                Удалить филиал
              </v-btn>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col cols="7">
        <v-card>
          <v-card-title class="subtitle-1">Редактировать информацию о филиале</v-card-title>
          <v-card-text>
            <EditBranchForm
              v-if="!!branchInfo"
              :companyUuid="companyUuid"
              :branchUuid="branchUuid"
              @onReload="reloadData()"
              ref="editBranchForm"
            ></EditBranchForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="subtitle-1">Сотрудники филиала</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="8">
                  <v-text-field
                    v-model="searchEmployee"
                    label="Поиск сотрудника"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-card-actions>
                  <v-dialog
                    v-model="dialog"
                    max-width="600px"
                    @click:outside="resetEmployeeCreateForm()"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        color="primary"
                        v-bind="attrs"
                        v-on="on"
                      >
                        Добавить работника
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="subtitle-1">
                        Добавить нового работника
                      </v-card-title>
                      <v-card-text>
                        <EmployeeCreateForm
                          :companyUuid="companyUuid"
                          :branchUuid="branchUuid"
                          ref="employeeCreateForm"
                          @onReload="reloadData()"
                        ></EmployeeCreateForm>
                      </v-card-text>
                    </v-card>
                  </v-dialog>
                  </v-card-actions>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <EmployeeListTable
                    ref="employeeListTable"
                    :search="searchEmployee"
                    :employeeList="branchInfo.employees"
                    @onReload="reloadData()"
                  ></EmployeeListTable>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {branchesApi} from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import BranchStatusForm from '@/core/components/branches/BranchStatusForm';
import EditBranchForm from '@/core/components/branches/EditBranchForm';
import EmployeeListTable from '@/core/components/employees/EmployeeListTable';
import EmployeeCreateForm from '@/core/components/employees/EmployeeCreateForm';

export default {
  components: {
    BranchStatusForm: BranchStatusForm,
    EditBranchForm: EditBranchForm,
    EmployeeListTable: EmployeeListTable,
    EmployeeCreateForm: EmployeeCreateForm
  },
  data() {
    return {
      branchInfo: null,
      searchEmployee: ''
    }
  },
  async mounted() {
    this.branchInfo = await this.getBranchInfo();
    await this.$nextTick(() => {
      this.$refs.editBranchForm.setInitial(this.branchInfo);
    });
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
    },
    async reloadData() {
      this.branchInfo = await this.getBranchInfo();
      this.$refs.editBranchForm.setInitial(this.branchInfo);
    },
    async deleteBranch() {
      const confirmParams = {
        message: `Вы действительно хотите удалить филиал ${this.branchInfo.address}?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(this.branchUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал удален!');
          this.$router.push({name: 'CompanyDetail', params: {companyUuid: this.companyUuid}});
        }
      });
    },
    resetEmployeeCreateForm() {
      this.$refs.employeeCreateForm.reset()
    }
  },
}
</script>