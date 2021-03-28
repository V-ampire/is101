<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="title">{{ employeeInfo.fio }}</h1>
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
              <IsActiveWidget
                v-if="!!employeeInfo.user"
                :isActive="employeeInfo.user.is_active"
                :accountUuid="employeeInfo.user.uuid"
                :accountRole="accountRole"
                ref="isActiveWidget"
                @onReload="reloadData"
              ></IsActiveWidget>
              <AccountEditForm
                v-if="!!employeeInfo.user" 
                :accountUuid="employeeInfo.user.uuid"
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
                        :accountUuid="employeeInfo.user.uuid"
                        :accountRole="accountRole"
                        @onReload="reloadData"
                      ></ChangePasswordForm>
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </div>
            </v-card-text>
          </v-card>
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">
              Статус работника
            </v-card-title>
            <v-card-text>
              <EmployeeStatusForm
                v-if="!!employeeInfo.status" 
                :companyUuid="companyUuid"
                :branchUuid="branchUuid"
                :employeeUuid="employeeUuid"
                :employeeStatus="employeeInfo.status"
                ref="employeeStatusForm"
                @onReload="reloadData"
              ></EmployeeStatusForm>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-title class="subtitle-1">Удалить работника</v-card-title>
            <v-card-subtitle class="body-2 text-wrap-normal">
              Информация о работнике будет удалена без возможности восстановления.
            </v-card-subtitle>
            <v-card-text>
              <v-btn 
                color="error"
                small
                block
                @click="deleteEmployee()"
              >
                Удалить работника
              </v-btn>
            </v-card-text>
          </v-card>

        </div>
      </v-col>
      <v-col cols="7">
        <v-card class="mb-3">
          <v-card-title class="subtitle-1">
            Редактировать информацию о работнике.
          </v-card-title>
          <v-card-text>
            <EmployeeEditForm
              v-if="!!employeeInfo"
              :companyUuid="companyUuid"
              :branchUuid="branchUuid"
              :employeeUuid="employeeUuid"
              ref="employeeEditForm"
              @onReload="reloadData"
            ></EmployeeEditForm>
          </v-card-text>
        </v-card>
        <v-card class="mb-3">
          <v-card-title class="subtitle-1">
            Изменить должность работника.
          </v-card-title>
          <v-card-text>
            <EmployeeChangePositionForm
              v-if="!!employeeInfo"
              :companyUuid="companyUuid"
              :branchUuid="branchUuid"
              :employeeUuid="employeeUuid"
              :currentPosition="employeeInfo.position"
              ref="employeeChangePosition"
              @onReload="reloadData"
            ></EmployeeChangePositionForm>
          </v-card-text>
        </v-card>
        <v-card>
          <v-card-title class="subtitle-1">
            Филиал
          </v-card-title>
          <v-card-text>
            <EmployeeChangeBranchForm
              v-if="!!employeeInfo" 
              :companyUuid="companyUuid"
              :employeeUuid="employeeUuid"
              :currentBranch="employeeInfo.branch"
              ref="employeeChangeBranch"
              @onReload="reloadData"
              :key="componentKey"
            ></EmployeeChangeBranchForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import roles from '@/core/services/roles';
import { employeesApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import AccountEditForm from '@/core/components/accounts/AccountEditForm';
import IsActiveWidget from '@/core/components/accounts/IsActiveWidget';
import ChangePasswordForm from '@/core/components/accounts/ChangePasswordForm';
import EmployeeEditForm from '@/core/components/employees/EmployeeEditForm';
import EmployeeStatusForm from '@/core/components/employees/EmployeeStatusForm';
import EmployeeChangePositionForm from '@/core/components/employees/EmployeeChangePositionForm';
import EmployeeChangeBranchForm from '@/core/components/employees/EmployeeChangeBranchForm';


export default {
  components: {
    AccountEditForm: AccountEditForm,
    IsActiveWidget: IsActiveWidget,
    ChangePasswordForm: ChangePasswordForm,
    EmployeeEditForm: EmployeeEditForm,
    EmployeeStatusForm: EmployeeStatusForm,
    EmployeeChangePositionForm: EmployeeChangePositionForm,
    EmployeeChangeBranchForm: EmployeeChangeBranchForm
  },
  data() {
    return {
      employeeInfo: null,
      accountRole: roles.employee[0],
      changeBranchKey: 0,
    }
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    },
    employeeUuid() {
      return this.$route.params.employeeUuid;
    },
    branchUuid() {
      return this.$route.params.branchUuid;
    },
    companyUuid() {
      return this.$route.params.companyUuid;
    },
  },
  async mounted() {
    this.employeeInfo = await this.getEmployeeInfo();
    await this.$nextTick(() => {
      this.$refs.accountEditForm.setInitial(this.employeeInfo.user);
      this.$refs.employeeEditForm.setInitial(this.employeeInfo);
    });
  },
  watch: {
    $route: 'reloadData'
  },
  methods: {
    async getEmployeeInfo() {
      let response;
      try {
        response = await this.api.detail(this.employeeUuid);
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (response.data.uuid == this.employeeUuid) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о работнике. Получен ответ ${response}`);
      }
    },
    async deleteEmployee() {
      const confirmParams = {
        message: `Вы действительно хотите удалить работника ${this.employeeInfo.fio}?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(this.employeeInfo.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Рвботник удален!');
          this.$router.push({
            name: 'BranchDetail', 
            params: {companyUuid: this.companyUuid, branchUuid: this.branchUuid}
          });
        }
      });
    },
    async reloadData() {
      this.employeeInfo = await this.getEmployeeInfo();
      this.$refs.accountEditForm.setInitial(this.employeeInfo.user);
      this.$refs.employeeEditForm.setInitial(this.employeeInfo);
    },
  }
}
</script>

