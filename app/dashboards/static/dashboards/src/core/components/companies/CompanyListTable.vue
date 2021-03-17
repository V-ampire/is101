<template>
  <!-- <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getStatusClasses"
    :sort-by="status"
    :search="search"
  >
    <template v-slot:item.actions="{ item }">
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
      <div class="detail-link">
        <router-link
          :to="{ name: 'CompanyDetail', params: { companyUuid: item.uuid }}"
        >{{ item.title }}</router-link>
      </div>
    </template>
  </v-data-table> -->
  <ListTable
    :headers="headers"
    :items="items"
    :search="search"
  >
      <template v-slot:itemLink="{ item }">
      <div class="detail-link">
        <router-link
          :to="{ name: 'CompanyDetail', params: { companyUuid: item.uuid }}"
        >{{ item.linkText }}</router-link>
      </div>
      </template>
  </ListTable>
</template>

<script>
/* Таблица со списком юр. лиц */
import companiesApi from "@/core/services/http/companies";
import statuses from "@/core/services/statuses";
import eventUtils from '@/core/services/events/utils';
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import ListTable from '@/core/components/commons/ListTable';

export default {
  mixins: [statusClassesMixin],
  components: {
    ListTable: ListTable
  },
  data () {
    return {
      headers: [
        {text: 'Название юр. лица', value: 'linkText'},
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
  computed: {
    items () {
      let result = [];
      for (let company of this.companiesList) {
        result.push({
          linkText: company.title,
          city: company.city,
          address: company.address,
          status: statuses[company.status],
          url: company.url,
          uuid: company.uuid
        });
      }
      return result
    }
  },
  async mounted () {
    this.companiesList = await this.getCompanies();
  },
  methods: {
    async getCompanies() {
      let response;
      try {
        response = await companiesApi.list();
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        const errorMessage = 'Не удалось загрузить данные с сервера.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список юрлиц. Получен ответ ${response}`);
      }
    },
    async reloadCompanies() {
      this.companiesList = await this.getCompanies();
    },
    deleteCompany(company) {
      const confirmParams = {
        message: `Вы действительно хотите удалить юрлицо ${company.title}`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.delete(company.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо удалено!');
          eventUtils.reloadData();
        }
      });
    },
    toAchiveCompany(company) {
      const message = `Вы действительно хотите перевести в архив юрлицо ${company.title}?
      В этом случае все филиалы и работники юрлица также будут переведены в архив.`;

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.toArchive(company.uuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо переведено в архив!');
          eventUtils.reloadData();
        }
      });
    },
    toWorkCompany(company) {
      const confirmParams = {
        message: `Вы действительно хотите вернуть юрлицо ${company.title} в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await companiesApi.toWork(company.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо в работе!');
          eventUtils.reloadData();
        }
      });
    }
  },
}
</script>