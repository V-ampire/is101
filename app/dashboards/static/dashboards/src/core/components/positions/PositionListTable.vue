<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :sort-by="status"
    :search="search"
    :item-class="getStatusClasses"
  >
    <template v-slot:item.actions="{ item }">
      <div class="action-icons d-flex">
        <div class="delete-btn mr-1">
          <v-tooltip left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="deleteItem(item)"
              >
                <v-icon small>fa-trash-alt</v-icon>
              </v-btn>
            </template>
            Удалить
          </v-tooltip>
        </div>
        <div class="edit-btn">
          <v-dialog
            v-model="item.editDialog"
            max-width="600px"
            @click:outside="resetEditPositionForm()"
          >
            <template v-slot:activator="{ on, attrs }">
              <div class="edit-btn-tooltip" v-bind="attrs" v-on="on">
                <v-tooltip left>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      color="primary"
                      x-small
                      fab
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon small>fa-edit</v-icon>
                    </v-btn>
                  </template>
                  Редактировать
                </v-tooltip>
              </div>
            </template>
            <v-card>
              <v-card-title class="subtitle-1">Изменить должность</v-card-title>
              <v-card-text>
                <PositionEditForm
                  ref="positionEditForm"
                  :position="item"
                  @onReload="reloadPositionList()"
                ></PositionEditForm>
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>
      </div>
    </template>
  </v-data-table>
</template>


<script>
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import statuses from "@/core/services/statuses";
import { positionsApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import PositionEditForm from '@/core/components/positions/PositionEditForm';

export default {
  mixins: [statusClassesMixin],
  components: {
    PositionEditForm: PositionEditForm
  },
  props: {
    search: String
  },
  data() {
    return {
      positionList: [],
      headers: [
        {text: 'Должность', value: 'title'},
        //{text: 'Статус', value: 'status'},
        {text: 'Действия', value: 'actions', sortable: false}
      ],
      statuses: statuses,
    }
  },
  computed: {
    items() {
      let result = [];
      for (let position of this.positionList) {
        result.push({
          title: position.title,
          status: statuses[position.status],
          uuid: position.uuid,
          editDialog: false
        });
      }
      return result
    },
  },
  async mounted() {
    this.positionList = await this.getPositions()
  },
  methods: {
    async reloadPositionList() {
      this.positionList = await this.getPositions()
    },
    async getPositions() {
      let response;
      try {
        response = await positionsApi().list();
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        const errorMessage = 'Не удалось загрузить данные с сервера.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список должностей. Получен ответ ${response}`);
      }
    },
    deleteItem(position) {
      const confirmParams = {
        message: `Вы действительно хотите удалить должность ${position.title}`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await positionsApi().delete(position.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Должность удалена!');
          this.reloadPositionList();
        }
      });

    },
    resetEditPositionForm() {
      this.$refs.positionEditForm.reset();
    }
  },
}
</script>