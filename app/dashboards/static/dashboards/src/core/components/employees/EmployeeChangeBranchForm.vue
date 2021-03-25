<template>
  <v-form ref="form">
    <div class="branch-current mb-2">
      <h3 class="mb-2">{{ currentBranch.city }}, {{ currentBranch.address }}</h3>
      <div class="body-1">Тел. {{ currentBranch.phone }}</div>
    </div>
    <div class="branch-field">
      <div class="branch-field-label subtitle-2 mb-2">Выберите новый филиал</div>
      <div class="branch-field-input">
        <v-select
          v-model="fields.branch.value"
          :items="branchItems"
          item-text="address"
          item-value="uuid"
          :placeholder="currentBranch.address"
          :error-messages="fields.branch.errors"
        ></v-select>
      </div>
    </div>
    <div class="form-btn">
      <FormButton
        label="Изменить филиал"
        :inProgress="inProgress"
        @onAction="changeBranch()"
      ></FormButton>
    </div>
  </v-form>
</template>


<script>
import { employeesApi, branchesApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import { ServerError } from '@/core/services/errors/types';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [formFieldsMixin],
  components: {
    FormButton: FormButton
  },
  props: {
    currentBranch: Object,
    companyUuid: String,
    employeeUuid: String,
  },
  data() {
    return {
      fields: {
        branch: {value: this.currentBranch.uuid, errors: []}
      },
      branchList: [],
      inProgress: false
    }
  },
  async mounted() {
    this.branchList = await this.getBranches();
  },
  watch: {
    async currentBranch() {
      this.branchList = await this.getBranches();
    } 
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.currentBranch.uuid)
    },
    branchItems() {
      let items = [];
      for (let branch of this.branchList) {
        if (branch.uuid !== this.currentBranch.uuid) {
          items.push({
            address: branch.address,
            uuid: branch.uuid,
          })
        }
      }
      return items
    }
  },
  methods: {
    async getBranches() {
      let response;
      try {
        response = await branchesApi(this.companyUuid).list('works')
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        const errorMessage = 'Не удалось загрузить список филталов.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список филиалов. Получен ответ ${response}`);
      }
    },
    async changeBranch() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await this.api.changeBranch(this.employeeUuid, formData)
        } catch (err) {
          if (err instanceof ServerError) {
            for (let field of Object.keys(err.data)) {
              this.setErrorMessages(field, err.data[field])
            }
          } else {
            eventUtils.showErrorAlert(err.message);
          }
          throw err
        } finally {
          this.inProgress = false;
        }
        eventUtils.showSuccessEvent('Данные изменены!');
        this.$router.push({
          name: 'EmployeeDetail', 
          params: {
            companyUuid: this.companyUuid,
            branchUuid: this.fields.branch.value,
            employeeUuid: this.employeeUuid
          }
        })
      }
    }
  },
}
</script>