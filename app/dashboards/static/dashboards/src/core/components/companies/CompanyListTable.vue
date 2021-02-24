<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getRowClasses"
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
    <template v-slot:item.title="{ item }">
      <a v-if="item.status==statuses.works" href="#">{{ item.title }}</a>
      <span v-else>{{ item.title }}</span>
    </template>
  </v-data-table>
</template>

<script>
/* Таблица со списком юр. лиц */
import companiesApi from "@/core/services/http/companies";
import statuses from "@/core/services/statuses";
import utils from '@/core/services/events/utils';
import { processHttpError } from '@/core/services/errors/utils';

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
      companiesList: [],
      statuses: statuses
    }
  },

  props: {
    search: String
  },

  mounted () {
    this.getCompanies();
  },

  methods: {
    getRowClasses: function(item) {
      if (item.status == statuses.archived) {
        return 'archive'
      }
    },
    async getCompanies() {
      let response;
      try {
        response = await companiesApi.list();
      } catch (err) {
        return processHttpError(err);
      }
      const companiesData = response.data;
      if (Array.isArray(companiesData)) {
        this.companiesList = companiesData;
      } else {
        const errorMessage = 'Не удалось загрузить данные с сервера.';
        utils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список юрлиц. Получен ответ ${response}`);
      }
    },
    deleteCompany(company) {
      const confirmParams = {
        message: `Вы действительно хотите удалить юрлицо ${company.title}`
      }
      utils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.delete(company.uuid);
          } catch (err) {
            return processHttpError(err);
          }
          this.getCompanies();
        }
      });
    },
    toAchiveCompany(company) {
      const message = `Вы действительно хотите перевести в архив юрлицо ${company.title}?
      В этом случае все филиалы и работники юрлица также будут переведены в архив.`;

      const confirmParams = {
        message: message
      }
      utils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.toArchive(company.uuid, true);
          } catch (err) {
            return processHttpError(err);
          }
          this.getCompanies();
        }
      });
    },
    toWorkCompany(company) {
      const confirmParams = {
        message: `Вы действительно хотите вернуть юрлицо ${company.title} в работу?`
      }
      utils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.toWork(company.uuid);
          } catch (err) {
            return processHttpError(err);
          }
          this.getCompanies();
        }
      });
    }
  },
  computed: {
    items: function() {
      let result = [];
      // FIXME обработать случай с отсутствием ключей
      for (let company of this.companiesList) {
        result.push({
          title: company.title,
          city: company.city,
          address: company.address,
          status: statuses[company.status],
          url: company.url,
          uuid: company.uuid
        });
      }
      return result
    }
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

</style>