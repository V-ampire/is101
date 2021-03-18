<template>
  <v-card class="mx-4">
    <v-card-title>Юридические лица</v-card-title>
    <v-container>
      <v-row>
        <v-col cols="8">
          <v-text-field
            v-model="search"
            label="Поиск юрлица"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-card-actions>
            <v-dialog
              v-model="dialog"
              max-width="600px"
              @click:outside="resetCreateCompanyForm()"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                >
                  Добавить юрлицо
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="subtitle-1">Добавить новое юрлицо</v-card-title>
                <v-card-text>
                  <CreateCompanyForm
                    ref="createCompanyform"
                    @onReload="reloadCompanyList()"
                  ></CreateCompanyForm>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-card-actions>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <CompanyListTable
            ref="companyListTable"
            v-bind:search="search"
          ></CompanyListTable>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
/*
Вью для отображения списка компаний.
*/
import CompanyListTable from '@/core/components/companies/CompanyListTable';
import CreateCompanyForm from '@/core/components/companies/CreateCompanyForm';

export default {
  data () {
    return {
      search: '',
    }
  },
  components: {
    CompanyListTable: CompanyListTable,
    CreateCompanyForm: CreateCompanyForm
  },
  methods: {
    resetCreateCompanyForm() {
      this.$refs.createCompanyform.reset();
    },
    reloadCompanyList() {
      this.$refs.companyListTable.reloadCompanies();
    }
  },
}
</script>