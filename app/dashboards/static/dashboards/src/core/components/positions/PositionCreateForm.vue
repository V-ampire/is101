<template>
  <v-form ref="form">
    <div class="form-fields d-flex flex-column mb-3">
      <div class="title-field">
        <div class="title-field-label subtitle-2 mb-2">Название должности</div>
        <div class="title-field-input">
          <v-text-field
            v-model="fields.title.value"
            :error-messages="fields.title.errors"
            :rules="[rules.required]"
            label="Название должности"
            name="title"
            counter
          ></v-text-field>
        </div>
      </div>
    </div>
    <div class="form-btn mb-3">
      <FormButton
        label="Добавить должность"
        :inProgress="inProgress"
        @onAction="create()"
      ></FormButton>
    </div>
  </v-form>
</template>

<script>
import createFormMixin from '@/core/mixins/createFormMixin';
import validators from '@/core/validators';
import { positionsApi } from '@/core/services/http/clients';
import FormButton from '@/core/components/commons/FormButton';
import eventUtils from '@/core/services/events/utils';

export default {
  mixins: [createFormMixin],
  components: {
    FormButton: FormButton
  },
  data() {
    return {
      fields: { title: {value: '', errors: []} },
      rules: {
        required: validators.required('Обязательное поле.'),
      },
    }
  },
  computed: {
    api() {
      return positionsApi()
    }
  },
  methods: {
    afterCreate(positionData) {
      eventUtils.showSuccessEvent('Должность добавлена.');
      return positionData
    }
  },
}
</script>