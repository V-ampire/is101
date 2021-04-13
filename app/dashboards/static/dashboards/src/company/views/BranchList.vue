<template>
  <v-card class="mx-4">
    <v-card-title>Филиалы</v-card-title>
     <v-container>
      <v-row>
        <v-col cols="8">
          <v-text-field
            v-model="search"
            label="Поиск филиала"
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
                  Добавить филиал
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="subtitle-1">Добавить новый филиал</v-card-title>
                <v-card-text>
                  <BranchCreateForm
                    :companyUuid="companyUuid"
                    ref="branchCreateForm"
                    @onReload="reloadData"
                  ></BranchCreateForm>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-card-actions>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <BranchListTable
            :branchList="branchList"
            :companyUuid="companyUuid"
            ref="branchListTable"
            v-bind:search="search"
            @onReload="reloadData"
          ></BranchListTable>
        </v-col>
      </v-row>

    </v-container>
  </v-card>
</template>

<script>
import { branchesApi } from '@/core/services/http/clients';
import config from '@/config';
import eventUtils from '@/core/services/events/utils';

import BranchListTable from '@/core/components/branches/BranchListTable';
import BranchCreateForm from '@/core/components/branches/BranchCreateForm';

export default {
  components: {
    BranchListTable: BranchListTable,
    BranchCreateForm: BranchCreateForm
  },
  data() {
    return {
      search: '',
      branchList: []
    }
  },
  computed: {
    companyUuid() {
      return this.$cookies.get(config.profileUuidCookie)
    },
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  async mounted() {
    this.branchList = await this.getBranchList();
  },
  methods: {
    async getBranchList() {
      let response;
      try {
        response = await this.api.list();
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось загрузить список филиалов. Получен ответ ${response}`);
      }
    },
    async reloadData() {
      this.branchList = await this.getBranchList();
    }
  }
}
</script>