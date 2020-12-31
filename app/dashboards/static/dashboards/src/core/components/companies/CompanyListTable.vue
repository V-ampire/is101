<template>
  <v-data-table
    :headers="headers"
    :items="companies"
    :item-class="getRowClasses"
    :sort-by="status"
    :search="search"
  >
    <template v-slot:item.actions="{ item }">
      <!-- Колонка с кнопками редактирования и удаления -->
      <!-- Показываем только для активных -->
      <div class="action-icons" v-if="item.status==statuses.active">
        <v-icon  
          small 
          class="mr-2" 
          @click="editCompany(item.uuid)"
        >
          mdi-pencil
        </v-icon>
        <v-icon 
          v-if="item.status==statuses.active" 
          small
          @click="deleteCompany(item.uuid)"
        >
          mdi-delete
        </v-icon>
      </div>
    </template>
    <template v-slot:item.title="{ item }">
      <a v-if="item.status==statuses.active" href="#">{{ item.title }}</a>
      <span v-else>{{ item.title }}</span>
    </template>
  </v-data-table>
</template>

<script>
/* Таблица со списком юр. лиц */
import copmaniesApi from "@/core/services/http/companies";

export default {
  data () {
    return {
      headers: [
        {text: 'Название юр. лица', value: 'title'},
        {text: 'Город', value: 'city' },
        {text: 'Адрес', value: 'address' },
        {text: 'Статус', value: 'status' },
        {text: 'Действия', value: 'actions', sortable: false}
      ],
      companies: [],
      statuses: {
        active: 1,
        archive: 0
      }
    }
  },
  props: {
    search: String
  },
  mounted () {
    this.getCompanies();
  },
  methods: {
    getCompanies () {
      copmaniesApi.getAll()
        .then(response => {
          this.companies = response.data;
        })
    },
    editCompany (companyUuid) {
      console.log(companyUuid)
    },
    deleteCompany (companyUuid) {
      console.log(companyUuid)
    },
    getRowClasses: function(item) {
      if (item.status == this.statuses.archive) {
        return 'archive'
      }
    },
  }
}
</script>


<style>
  .archive {
  background-color:red;
  color: white;
  opacity: 0.5;
  pointer-events: none;
}

.archive a {
  cursor: not-allowed;
  color: white;
}

</style>