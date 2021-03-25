<template>
  <v-form ref="form">
    <div class="position-current mb-2">
      <h3 class="mb-2">{{ currentPosition.title }}</h3>
    </div>
    <div class="position-field">
      <div class="position-field-label subtitle-2 mb-2">Выберите новую должность</div>
      <div class="position-field-input">
        <v-select
          v-model="fields.position.value"
          :items="positionItems"
          item-text="title"
          item-value="uuid"
          :placeholder="currentPosition.title"
          :error-messages="fields.position.errors"
        ></v-select>
      </div>
    </div>
    <div class="form-btn">
      <FormButton
        label="Изменить должность"
        :inProgress="inProgress"
        @onAction="changePosition()"
      ></FormButton>
    </div>
  </v-form>
</template>

<script>
import { employeesApi, positionsApi } from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import { ON_RELOAD } from '@/core/services/events/types';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import { ServerError } from '@/core/services/errors/types';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [formFieldsMixin],
  components: {
    FormButton: FormButton
  },
  props: {
    currentPosition: Object,
    companyUuid: String,
    branchUuid: String,
    employeeUuid: String,
  },
  data() {
    return {
      fields: {
        position: {value: this.currentPosition.uuid, errors: []}
      },
      positionList: [],
      inProgress: false
    }
  },
  async mounted() {
    this.positionList = await this.getPositions();
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    },
    positionItems() {
      let items = [];
      for (let position of this.positionList) {
        if (position.uuid !== this.currentPosition.uuid) {
          items.push({
            title: position.title,
            uuid: position.uuid,
          })
        }
      }
      return items
    }
  },
  methods: {
    async getPositions() {
      let response;
      try {
        response = await positionsApi().list('works')
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        const errorMessage = 'Не удалось загрузить список должностей.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список должностей. Получен ответ ${response}`);
      }
    },
    async changePosition() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await this.api.changePosition(this.employeeUuid, formData)
        } catch (err) {
          if (err instanceof ServerError) {
            for (let field of Object.keys(err.data)) {
              this.setErrorMessages(field, err.data[field])
            }
          } else {
            eventUtils.showErrorAlert(err.message);
          }
          throw err
        } finally {
          this.inProgress = false;
        }
        eventUtils.showSuccessEvent('Данные изменены!');
        this.$emit(ON_RELOAD);
      }
    }
  },
}
</script>