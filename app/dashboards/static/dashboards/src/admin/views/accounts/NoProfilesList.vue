<template>
  <v-container>
    <v-card>
      <v-card-title>
        Учетные записи с пустым профилем
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="items"
        :search="search"
      ></v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import accountsApi from '@/core/services/http/accounts';
import utils from '@/core/services/events/utils';
import roles from '@/core/services/accounts/roles';

export default {
  data: () => ({
    search: '',
    accountsList: [],
    headers: [
      {text: 'Имя пользователя', align: 'start', value: 'username'},
      {text: 'Тип учетной записи', value: 'role'},
      {text: 'Статус', value: 'isActive'}
    ],
  }),

  mounted() {
    this.getNoProfiles();
  },

  computed: {
    items: function() {
      let result = [];
      // FIXME обработать случай с отсутствием ключей
      for (let account of this.accountsList) {
        const accountStatus = account.is_active ? 'Доступ разрешен' : 'Доступ запрещен';
        result.push({
          username: account.username,
          role: roles[account.role],
          isActive: accountStatus
        });
      }
      return result
    }
  },

  methods: {
    async getNoProfiles() {
      let response = await accountsApi.noProfiles.list();
      const accountsData = response.data;
      if (Array.isArray(accountsData)) {
        this.accountsList = accountsData;
      } else {
        const errorMessage = 'Не удалось загрузить данные с сервера.';
        utils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список аккаунтов без профилей. Получен ответ ${response}`);
      }
    }
  },
}
</script>