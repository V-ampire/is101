<template>
  <v-app>
    <v-main>
      <router-link
        to='/dashboards/about'
        tag='span'
        style='cursor: pointer'>
        About
      </router-link>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  components: {
    
  },

  data: () => ({
    //
  }),
};
</script>
