<template>
  <ListTable
    :headers="headers"
    :items="items"
    :search="search"
    @onToArchiveItem="toArchiveEmployee"
    @onToWorkItem="toWorkEmployee"
    @onDeleteItem="deleteEmployee"
  >
    <template v-slot:itemLink="{ item }">
      <div class="detail-link body-2">
        <router-link
          :to="{ name: 'EmployeeDetail', 
          params: { companyUuid: companyUuid, branchUuid: branchUuid, employeeUuid: item.uuid }}"
        >{{ item.linkText }}</router-link>
      </div>
    </template>
  </ListTable>
</template>


<script>
import statuses from "@/core/services/statuses";
import eventUtils from '@/core/services/events/utils';
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import ListTable from '@/core/components/commons/ListTable';
import {employeesApi} from '@/core/services/http/clients';

export default {
  mixins: [statusClassesMixin],
  components: {
    ListTable: ListTable
  },
  props: {
    search: String,
    employeeList: Array,
    companyUuid: String,
    branchUuid: String
  },
  data() {
    return {
      headers: [
        {text: 'ФИО', value: 'linkText'},
        {text: 'Должность', value: 'position' },
        {text: 'Статус', value: 'status' },
        {text: 'Действия', value: 'actions', sortable: false}
      ],
    }
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    },
    items() {
      let result = [];
      for (let employee of this.employeeList) {
        result.push({
          linkText: employee.fio,
          position: employee.position.title,
          status: statuses[employee.status],
          uuid: employee.uuid
        });
      }
      return result
    },
  },
  methods: {
    async toArchiveEmployee(employee) {
      const message = 'Вы действительно хотите перевести работника в архив?';

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toArchive(employee.uuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Работник переведен в архив. Учетная запись отключена.');
          this.$emit('onReload');
        }
      });
    },
    async toWorkEmployee(employee) {
      const confirmParams = {
        message: `Вы действительно хотите вернуть работника в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toWork(employee.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Работник в работе.');
          this.$emit('onReload');
        }
      });
    },
    async deleteEmployee(employee) {
      const confirmParams = {
        message: `Вы действительно хотите удалить работника ${employee.fio}?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(employee.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Работник удален!');
          this.$emit('onReload');
        }
      });
    }
  }
}
</script>