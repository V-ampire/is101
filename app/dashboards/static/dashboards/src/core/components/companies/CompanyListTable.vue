<template>
  <ListTable
    :headers="headers"
    :items="items"
    :search="search"
    @onToArchiveItem="toAchiveCompany"
    @onToWorkItem="toWorkCompany"
    @onDeleteItem="deleteCompany"
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
        message: `Вы действительно хотите удалить юрлицо ${company.linkText}`
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
          this.reloadCompanies();
        }
      });
    },
    toAchiveCompany(company) {
      const message = `Вы действительно хотите перевести в архив юрлицо ${company.linkText}?
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
          this.reloadCompanies();
        }
      });
    },
    toWorkCompany(company) {
      const confirmParams = {
        message: `Вы действительно хотите вернуть юрлицо ${company.linkText} в работу?`
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
          this.reloadCompanies();
        }
      });
    }
  },
}
</script>