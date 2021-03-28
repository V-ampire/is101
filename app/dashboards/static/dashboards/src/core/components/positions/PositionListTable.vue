<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :sort-by="status"
    :search="search"
    :item-class="getStatusClasses"
  >
    <template v-slot:item.title="{ item }">
      <div v-if="editState" class="title-edit">
        <v-text-field dense></v-text-field>
      </div>
      <div v-else class="title-value dotted" @click="!editState">
        {{ item.title }}
      </div>
    </template>
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
        <div class="delete-btn">
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
      </div>
    </template>

  </v-data-table>
</template>


<script>
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import statuses from "@/core/services/statuses";

export default {
  mixins: [statusClassesMixin],
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
      editState: false
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

    }
  },
  async mounted() {
    this.positionList = await this.getPositions()
  },
  methods: {
    reloadPositions() {
      this.positionList = await this.getPositions()
    },
    async getPositions() {
      
    },
    toArchiveItem(item) {

    },
    toWorkItem(item) {

    },
    deleteItem(item) {

    }
  },
}
</script>

<style>
  .dotted {
    text-decoration: underline;
    text-decoration-style: dotted;
  }
</style>