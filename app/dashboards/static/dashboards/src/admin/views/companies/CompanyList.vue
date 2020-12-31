<template>
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
            <CreateCompanyDialog/>
          </v-card-actions>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <CompanyListTable v-bind:search="search"/>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
/*
Вью для отображения списка компаний.
*/
import CompanyListTable from '@/core/components/companies/CompanyListTable'
import CreateCompanyDialog from '@/core/components/companies/CreateCompanyDialog'

export default {
  data () {
    return {
      search: '',
    }
  },
  components: {
    CompanyListTable,
    CreateCompanyDialog
  }
}
</script>