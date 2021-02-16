<template>
  <v-app>
    <div class="alerts">
      <ErrorAlert ref="errorAlert"></ErrorAlert>
    </div>
    <div class="modals">
      <ConfirmDialog ref="confirm"></ConfirmDialog>
    </div>
    <v-main>
    </v-main>
  </v-app>
</template>

<script>
import ConfirmDialog from '@/core/components/commons/ConfirmDialog'
import ErrorAlert from '@/core/components/commons/ErrorAlert'
import CompanyList from '@/admin/views/companies/CompanyList'
import { ON_APP_ERROR } from '@/core/events/types'
import eventBus from '@/core/events/eventBus'

export default {
  name: 'App',

  components: {
    'ConfirmDialog': ConfirmDialog,
    //'CompanyList': CompanyList,
    'ErrorAlert': ErrorAlert
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
    },
    showAlert() {
      eventBus.$emit(ON_APP_ERROR, {message: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Numquam labore ipsa exercitationem inventore excepturi ex nulla. Blanditiis dolore explicabo totam atque enim, rem est ipsum labore iusto tenetur minus commodi."})
    }
  },
};
</script>
