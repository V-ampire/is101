<template>
  <v-form ref="form">
    <div class="status-info mb-2">
      <h3 class="mb-2">Текущий статус</h3>
      <span v-if="companyStatus=='works'">
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-briefcase</v-icon>
        </v-btn> - В работе
      </span>
      <span v-else>
        <v-btn color="primary" x-small fab>
          <v-icon small>fa-archive</v-icon>
        </v-btn> - В архиве
      </span>
    </div>
    <div class="form-btn">
      <div v-if="companyStatus=='works'" class="form-btn-toWork">
        <v-btn
          color="primary"
          small
          block
          @click="toArchve()"
        >
          <v-icon class="mr-2" small>fa-archive</v-icon> Перевести в архив
        </v-btn>
      </div>
      <div v-else class="form-btn-toArchive">
        <v-btn
          color="primary"
          small
          block
          @click="toWork()"
        >
          <v-icon class="mr-2" small>fa-briefcase</v-icon> Перевести в работу
        </v-btn>
      </div>
    </div>
  </v-form>
</template>

<script>
import companiesApi from '@/core/services/http/companies';
import eventUtils from '@/core/services/events/utils';

export default {
  props: {
    companyUuid: String,
    companyStatus: String
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