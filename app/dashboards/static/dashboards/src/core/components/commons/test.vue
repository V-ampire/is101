<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getStatusClasses"
    :sort-by="status"
    :search="search"
  >
    <template v-slot:item.actions="{ item }">
      <!-- Колонка с кнопками стандартных действий -->
      ...
    </template>
    <template v-slot:item.title="{ item }">
      <div class="detail-link">
        <router-link
          :to="{ name: 'Detail', params: { uuid: item.uuid }}"
        >{{ item.title }}</router-link>
      </div>
    </template>
</template>

Я использую vuetify для своего проекта, у меня в проект много таблиц в которых повторяются колонки со стандартными действиями, поэтому я хочу создать свой компонент поверх вьютифаевской data-table.
При этом в заголовках title нужно отображать ссылки на объекты  но чтобы получить эту ссылку из роутера мне нужно передать item таблицы.
