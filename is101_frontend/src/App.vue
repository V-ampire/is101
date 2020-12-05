<template>
  <v-app>
    <div class="modals">
      <confirmDlg ref="confirm"></confirmDlg>
    </div>
    <v-main>
      <v-btn color="red" dark @click="delRecord"> Delete this! </v-btn>
    </v-main>
  </v-app>
</template>

<script>
import ConfirmDialog from './components/base/ConfirmDialog';

export default {
  name: 'App',

  components: {
    'confirmDlg': ConfirmDialog
  },

  data: () => ({
    //
  }),
  methods: {
    delRecord () {
      this.$refs.confirm.open(
        "Удалить?", 
        "Подтвердите удаление",
      ).then((res => {
        console.log('Deleted!');
        console.log(res);
      }))
    }
  },
};
</script>
