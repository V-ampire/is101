<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getStatusClasses"
    :sort-by="status"
    :search="search"
  >
    <template v-slot:item.actions="{ item }">
      <!-- Колонка с кнопками архивирования/в работу и удаления -->
      <div class="action-icons d-flex">
        <div class="status-btn mr-1">
          <v-tooltip left v-if="item.status==statuses.works">
            <template v-slot:activator="{ on, attrs }">
              <v-btn  
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="toAchiveCompany(item)"
              >
                <v-icon small>fa-archive</v-icon>
              </v-btn>
            </template>
            В архив
          </v-tooltip>
          <v-tooltip left v-else>
            <template v-slot:activator="{ on, attrs }">
              <v-btn  
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="toWorkCompany(item)"
              >
                <v-icon small>fa-briefcase</v-icon>
              </v-btn>
            </template>
            В работу
          </v-tooltip>
        </div>
        <div class="delete-btn">
          <v-tooltip left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="deleteCompany(item)"
              >
                <v-icon small>fa-trash-alt</v-icon>
              </v-btn>
            </template>
            Удалить
          </v-tooltip>
        </div>
      </div>
    </template>
  </v-data-table>
</template>


<script>
import statuses from "@/core/services/statuses";
// import eventUtils from '@/core/services/events/utils';
import statusClassesMixin from '@/core/mixins/statusClassesMixin';

export default {
  mixins: [statusClassesMixin],
  props: {
    search: String,
    employeeList: String,
    branchUuid: String,
    companyUuid: String
  },
  data() {
    return {
      headers: [
        {text: 'ФИО', value: 'fio'},
        {text: 'Должность', value: 'position' },
        {text: 'Статус', value: 'status' },
        // {text: 'Действия', value: 'actions', sortable: false}
      ],
      statuses: statuses
    }
  },
  computed: {
    items() {
      let result = [];
      for (let employee of this.employeeList) {
        result.push({
          fio: employee.fio,
          position: employee.position,
          status: statuses[employee.status],
        });
      }
      return result
    }
  }

}
</script>