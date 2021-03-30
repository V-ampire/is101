<template>
  <v-card class="mx-4">
    <v-card-title>Должности</v-card-title>
    <v-container>
      <v-row>
        <v-col cols="8">
          <v-text-field
            v-model="search"
            label="Поиск должности"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-card-actions>
            <v-dialog
              v-model="createDialog"
              max-width="600px"
              @click:outside="resetCreatePositionForm()"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                >
                  Добавить должность
                </v-btn>
              </template>
              <v-card>
                <v-card-title class="subtitle-1">Добавить должность</v-card-title>
                <v-card-text>
                  <PositionCreateForm
                    ref="createPositionForm"
                    @onReload="reloadPositionList()"
                  ></PositionCreateForm>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-card-actions>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <PositionListTable
            ref="positionListTable"
            v-bind:search="search"
          ></PositionListTable>
        </v-col>
      </v-row>
    </v-container>
  </v-card>

</template>

<script>
import PositionListTable from '@/core/components/positions/PositionListTable';
import PositionCreateForm from '@/core/components/positions/PositionCreateForm';

export default {
  data () {
    return {
      search: '',
      createDialog: false
    }
  },
  components: {
    PositionListTable: PositionListTable,
    PositionCreateForm: PositionCreateForm
  },
  methods: {
    resetCreatePositionForm() {
      this.$refs.createPositionForm.reset();
    },
    reloadPositionList() {
      this.$refs.positionListTable.reloadPositionList();
      this.createDialog = false;
    }
  },

}
</script>