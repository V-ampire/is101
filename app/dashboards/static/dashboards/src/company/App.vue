<template>
  <v-app>
    <div class="modals">
      <ErrorAlert ref="errorAlert"></ErrorAlert>
      <SuccessAlert ref="successAlert"></SuccessAlert>
      <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    </div>
    <v-navigation-drawer permanent app absolute>
      <v-list>
        <v-list-item>
          <div class="profile">
            <router-link 
              :to="{name: 'Profile'}"
            >
              Мой профиль
            </router-link>
          </div>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item>
          <div class="branches">
            <router-link 
              :to="{name: 'BranchList'}"
            >
              Филиалы
            </router-link>
          </div>
        </v-list-item>
        <v-divider></v-divider>
        <v-divider></v-divider>
        <v-list-item>
          <div class="docs">
            Документация
          </div>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main app>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import ErrorAlert from '@/core/components/commons/ErrorAlert';
import SuccessAlert from '@/core/components/commons/SuccessAlert';
import ConfirmDialog from '@/core/components/commons/ConfirmDialog';


export default {
  name: 'App',

  data: () => ({
    //
  }),
  components: {
    'ErrorAlert': ErrorAlert,
    'SuccessAlert': SuccessAlert,
    'ConfirmDialog': ConfirmDialog
  },


};
</script>
