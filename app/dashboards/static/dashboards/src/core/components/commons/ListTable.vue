<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getStatusClasses"
    :sort-by="status"
    :search="search"
  >
    <template v-slot:item.actions="{ item }">
      <!-- Колонка с кнопками архивирования/в работу и удаления -->
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
    <slot name="itemLink"></slot>
    <!-- <template v-slot:item.linkText="{ item }">
      <div class="detail-link">
        <router-link
          :to="{ name: itemRouteName, params: itemRouteParams}"
        >{{ item.linkText }}</router-link>
      </div>
    </template> -->
  </v-data-table>
</template>

<script>
/**
 * Базовый компонент для таблиц сущностей приложения.
 * Предоставляет кнопки для архивации/деархивации и удаления объектов.
 * Объект должен содержать заголовок linkText - это значение будет текстом ссылки на страницу информации об объекте.
 */
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import statuses from "@/core/services/statuses";

export default {
  mixins: [statusClassesMixin],
  props: {
    headers: Array,
    items: Array,
    search: String,
  },
  data() {
    return {
      statuses: statuses
    }
  },
  methods: {
    toArchiveItem(item) {
      console.log('toArchiveItem')
      this.$emit('onToArchiveItem', item);
    },
    toWorkItem(item) {
      console.log('toWorkItem')
      this.$emit('onToWorkItem', item);
    },
    deleteItem(item) {
      console.log('deleteItem')
      this.$emit('onDeleteItem', item);
    },
  }
}
</script>
