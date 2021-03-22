<template>
  <v-navigation-drawer
    permanent
  >
    <v-list>
      <v-list-item>
        <div class="accounts d-flex">
          <div class="accounts-title mr-1 align-self-center">
            Учетные записи
          </div>
        </div>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item>
        <div class="companies">
          <router-link 
            to="/companies"
          >
            Юридические лица
          </router-link>
        </div>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import eventUtils from '@/core/services/events/utils';

export default {
  data: () => ({
    noProfileCount: 0,
  }),
  
  methods: {
    async getNoProfilesCount() {
      let response;
      try {
        response = await accounts.noProfiles.count();
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      const count = response.data.count;
      if (Number.isInteger(count)) {
        this.noProfileCount = count;
      } else {
        console.log(`Не удалось загрузить число аккаунтов без профилей. Получен ответ ${response}`);
      }
    }
  },
}
</script>