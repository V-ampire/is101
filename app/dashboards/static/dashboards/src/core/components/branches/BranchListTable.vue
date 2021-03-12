<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :item-class="getRowClasses"
    :sort-by="status"
    :search="search"
    dense
  >
    <template v-slot:item.address="{ item }">
      <div class="detail-link body-2">
        <router-link
          :to="{ name: 'BranchDetail', params: { companyUuid: this.companyUuid, branchUuid: item.uuid }}"
        >{{ item.title }}</router-link>
      </div>
    </template>

  </v-data-table>
</template>

<script>
import statuses from "@/core/services/statuses";
import statusClassesMixin from '@/core/mixins/statusClassesMixin';

export default {
  mixins: [statusClassesMixin],
  props: {
    branchList: Array,
    companyUuid: String
  },
  data () {
    return {
      headers: [
        {text: 'Адрес', value: 'address'},
      ],
      search: ''
    }
  },
  computed: {
    items() {
      let branches = [];
      for (let branch of this.branchList) {
        branches.push({
          address: branch.address,
          status: statuses[branch.status],
          uuid: branch.uuid
        })
      }
      return branches
    },
  },
  methods: {
    getRowClasses(item) {
      let classes = this.getStatusClasses(item);
      classes += ' caption';
      return classes
    }
  },
}
</script>