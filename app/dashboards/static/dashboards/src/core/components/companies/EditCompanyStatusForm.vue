<template>
</template>

<script>
import companiesApi from '@/core/services/http/companies';
import eventUtils from '@/core/services/events/utils';
import statusFormMixin from '@/core/mixins/statusFormMixin';

export default {
  mixins: [statusFormMixin],
  props: {
    companyUuid: String,
  },
  data () {
    return {

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
            await companiesApi.toArchive(this.companyUuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо переведено в архив. Доступ ограничен.');
          eventUtils.reloadData();
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
            await companiesApi.toWork(this.companyUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Юрлицо в работе. Доступ разрешен.');
          eventUtils.reloadData();
        }
      });
    },
  },
}
</script>