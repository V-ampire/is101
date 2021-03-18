<template>
  <StatusForm
    :currentStatus="companyStatus"
    @onToArchive="toArchve()"
    @onToWork="toWork()"
  ></StatusForm>
</template>

<script>
import {companiesApi} from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import StatusForm from '@/core/components/commons/StatusForm';

export default {
  components: {
    StatusForm: StatusForm
  },
  props: {
    companyUuid: String,
    companyStatus: String
  },
  data () {
    return {

    }
  },
  computed: {
    api() {
      return companiesApi()
    }
  },
  methods: {
    toArchve () {
      const message = `Вы действительно хотите перевести в архив юрлицо?
      В этом случае все филиалы и работники юрлица также будут переведены в архив.`;

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toArchive(this.companyUuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо переведено в архив. Доступ ограничен.');
          this.$emit('onReload');
        }
      });
    },
    toWork () {
        const confirmParams = {
        message: `Вы действительно хотите вернуть юрлицо в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toWork(this.companyUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо в работе. Доступ разрешен.');
          this.$emit('onReload');
        }
      });
    },
  },
}
</script>