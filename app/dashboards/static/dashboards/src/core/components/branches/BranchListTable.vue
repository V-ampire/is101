<template>
  <ListTable
    :headers="headers"
    :items="items"
    @onToArchiveItem="toAchiveBranch"
    @onToWorkItem="toWorkBranch"
    @onDeleteItem="deleteBranch"
  >
    <template v-slot:itemLink="{ item }">
      <div class="detail-link body-2">
        <router-link
          :to="{ name: 'BranchDetail', params: { companyUuid: companyUuid, branchUuid: item.uuid }}"
        >{{ item.linkText }}</router-link>
      </div>
    </template>
  </ListTable>
</template>

<script>
import statuses from "@/core/services/statuses";
import statusClassesMixin from '@/core/mixins/statusClassesMixin';
import ListTable from '@/core/components/commons/ListTable';
import {branchesApi} from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';

export default {
  mixins: [statusClassesMixin],
  components: {
    ListTable: ListTable
  },
  props: {
    branchList: Array,
    companyUuid: String
  },
  data () {
    return {
      headers: [
        {text: 'Адрес', value: 'linkText'},
        {text: 'Действия', value: 'actions', sortable: false}
      ],
    }
  },
  computed: {
    items() {
      let branches = [];
      for (let branch of this.branchList) {
        branches.push({
          linkText: branch.address,
          status: statuses[branch.status],
          uuid: branch.uuid
        })
      }
      return branches
    },
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  methods: {
    toAchiveBranch(branch) {
      const message = `Вы действительно хотите перевести в архив филиал?
      В этом случае все работники филиала также будут переведены в архив.`;

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toArchive(branch.uuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал переведен в архив.');
          this.$emit('onReload');
        }
      });
    },
    toWorkBranch(branch) {
      const confirmParams = {
        message: `Вы действительно хотите вернуть филиал в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toWork(branch.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал в работе.');
          this.$emit('onReload');
        }
      });
    },
    deleteBranch(branch) {
      const confirmParams = {
        message: `Вы действительно хотите удалить филиал ${branch.address}?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(branch.uuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал удален!');
          this.$emit('onReload');
        }
      });
    }
  },
}
</script>
