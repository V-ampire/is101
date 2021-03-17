<template>
  <StatusForm
    :currentStatus="branchStatus"
    @onToArchive="toArchive()"
    @onToWork="toWork()"
  ></StatusForm>
</template>

<script>
import eventUtils from '@/core/services/events/utils';
import StatusForm from '@/core/components/commons/StatusForm';
import branchesApi from '@/core/services/http/branches';

export default {
  components: {
    StatusForm: StatusForm
  },
  props: {
    companyUuid: String,
    branchUuid: String,
    branchStatus: String
  },
  data() {
    return {

    }
  },
  computed: {
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  methods: {
    toArchive () {
      const message = `Вы действительно хотите перевести в архив филиал?
      В этом случае все работники филиала также будут переведены в архив.`;

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toArchive(this.branchUuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал переведен в архив.');
          this.$emit('onReload');
        }
      });
    },
    toWork () {
        const confirmParams = {
        message: `Вы действительно хотите вернуть филиал в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toWork(this.branchUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал в работе.');
          eventUtils.reloadData();
        }
      });
    },
  },
}
</script>