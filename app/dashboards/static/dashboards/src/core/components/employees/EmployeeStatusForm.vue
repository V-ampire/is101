<template>
  <StatusForm
    :currentStatus="employeeStatus"
    @onToArchive="toArchve()"
    @onToWork="toWork()"
  ></StatusForm>
</template>


<script>
import { employeesApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import StatusForm from '@/core/components/commons/StatusForm';
import { ON_RELOAD } from '@/core/services/events/types';

export default {
  components: {
    StatusForm: StatusForm
  },
  props: {
    companyUuid: String,
    branchUuid: String,
    employeeUuid: String,
    employeeStatus: String
  },
  data () {
    return {

    }
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    }
  },
  methods: {
    toArchve () {
      const message = `Вы действительно хотите перевести в архив работника?
      В этом случае учетная запись работника будет заблокирована.`

      const confirmParams = {
        message: message
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toArchive(this.employeeUuid, true);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Работник переведен в архив. Доступ ограничен.');
          this.$emit(ON_RELOAD);
        }
      });
    },
    toWork () {
        const confirmParams = {
        message: `Вы действительно хотите вернуть работника в работу?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.toWork(this.employeeUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Работник в работе. Доступ разрешен.');
          this.$emit(ON_RELOAD);
        }
      });
    },
  },
}
</script>