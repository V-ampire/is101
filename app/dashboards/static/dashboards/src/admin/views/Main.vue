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
export default {
  
}
</script>