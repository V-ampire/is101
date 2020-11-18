<template>
<v-app>
  <v-main>
    <v-container>
      <company-list></company-list>
    </v-container>
  </v-main>
</v-app>
</template>

<script>
import CompanyList from '@/components/CompanyList'

export default {
  name: 'App',

  components: {
    'company-list': CompanyList
  },

  data: () => ({
    //
  }),
};
</script>
