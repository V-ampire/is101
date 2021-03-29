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
        <div class="status-btn mr-1">
          <v-tooltip left v-if="item.status==statuses.works">
            <template v-slot:activator="{ on, attrs }">
              <v-btn  
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="toArchiveItem(item)"
              >
                <v-icon small>fa-archive</v-icon>
              </v-btn>
            </template>
            В архив
          </v-tooltip>
          <v-tooltip left v-else>
            <template v-slot:activator="{ on, attrs }">
              <v-btn  
                color="primary"
                x-small
                fab
                v-bind="attrs"
                v-on="on"
                @click="toWorkItem(item)"
              >
                <v-icon small>fa-briefcase</v-icon>
              </v-btn>
            </template>
            В работу
          </v-tooltip>
        </div>
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
            v-model="dialog"
            max-width="600px"
            @click:outside="resetCreatePositionForm()"
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
        {text: 'Статус', value: 'status'},
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
          uuid: position.uuid
        });
      }
      return result
    },
    api() {
      return positionsApi()
    }
  },
  async mounted() {
    this.positionList = await this.getPositions()
  },
  methods: {
    async reloadPositions() {
      this.positionList = await this.getPositions()
    },
    async getPositions() {
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
        const errorMessage = 'Не удалось загрузить данные с сервера.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список должностей. Получен ответ ${response}`);
      }
    },
    toArchiveItem(item) {
      console.log(item)
    },
    toWorkItem(item) {
      console.log(item)
    },
    deleteItem(item) {
      console.log(item)
    },
    updateItem(item) {
      console.log(item)
    }
  },
}
</script>