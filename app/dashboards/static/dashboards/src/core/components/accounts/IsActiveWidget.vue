<template>
  <div class="isActive-field">
    <div class="isActive-field-label subtitle-2">Доступ в систему:</div>
    <div class="isActive-field-switch">
      <v-switch
        v-model="isActive"
        :label="isActive ? 'Доступ разрешен' : 'Доступ ограничен'"
        @change="changeSwitch"
      >
        <template v-slot:label>
          <span v-if="inProgress">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </span>
          <span class="green--text ml-2" v-else-if="isActive">
            <v-icon color="green">fa-check-circle</v-icon> Доступ разрешен
          </span>
          <span class="red--text ml-2" v-else>
            <v-icon color="red">fa-times-circle</v-icon> Доступ ограничен
          </span>
        </template>
      </v-switch>
    </div>
  </div>
</template>

<script>
import accountsApiMixin from '@/core/mixins/accountsApiMixin';
import { ON_RELOAD } from '@/core/services/events/types';
import eventUtils from '@/core/services/events/utils';

export default {
  mixins: [accountsApiMixin],
  props: {
    isActive: Boolean,
    accountUuid: String,
    inProgress: {
      type: Boolean,
      default: false
    },
  },
  methods: {
    async changeSwitch() {
      this.inProgress = true;
      try {
        if (this.isActive) {
        // Разблокировать
          await this.api.activate(this.accountUuid);
        } else {
          // Заблокировать
          await this.api.deactivate(this.accountUuid);
        }
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      } finally {
        this.inProgress = false;
        this.$emit(ON_RELOAD); // Для того чтобы отменить изменение свитча
      }
    }
  },
}
</script>