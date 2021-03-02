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
          <div class="accounts-alert">
            <router-link 
              to="/no_profiles"
              style="text-decoration: none;"
            >
              <v-btn
                class="accounts-alert-btn white--text"
                color="red"
                fab
                small
                v-show="noProfileCount > 0"
              >
                {{ noProfileCount }}
              </v-btn>
            </router-link>
            <v-tooltip
              right
              activator=".accounts-alert-btn"
            >
              Найдено {{ noProfileCount }} учетных записей с незаполненым профилем!
            </v-tooltip>
          </div>
        </div>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item>
        <router-link 
          to="/companies"
        >
          Юридические лица
        </router-link>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import accounts from '@/core/services/http/accounts';
import eventUtils from '@/core/services/events/utils';
import errorUtils from '@/core/services/errors/utils';

export default {
  data: () => ({
    noProfileCount: 0,
  }),
  
  mounted() {
    this.getNoProfilesCount()
  },

  methods: {
    async getNoProfilesCount() {
      let response;
      try {
        response = await accounts.noProfiles.count();
      } catch (err) {
        const httpError = errorUtils.checkHttpError(err);
        eventUtils.showErrorAlert(httpError.message);
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