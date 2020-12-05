<template>
  <v-container>
    <v-card>
      <v-card-title>Юридические лица</v-card-title>
      <v-container>
        <v-row>
          <v-col cols="8">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Поиск"
              single-line
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-card-actions>
              <v-btn
                color="primary"
              >
                Добавить юр. лицо
              </v-btn>
              <!-- <create-dialog v-on:companyCreated="processCreate"></create-dialog> -->
            </v-card-actions>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">

          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>

</template>

<script>
/*
Вью для отображения списка компаний.
*/
export default {
  data () {
    return {
      search: '',
    }
  },
}
</script>