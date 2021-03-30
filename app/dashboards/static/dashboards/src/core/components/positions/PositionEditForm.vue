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
        label="Изменить должность"
        :inProgress="inProgress"
        @onAction="update()"
      ></FormButton>
    </div>
  </v-form>
</template>

<script>
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import FormButton from '@/core/components/commons/FormButton';
import validators from '@/core/validators';
import { positionsApi } from '@/core/services/http/clients';
import { ON_RELOAD } from '@/core/services/events/types';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';

export default {
  mixins: [formFieldsMixin],
  components: {
    FormButton: FormButton
  },
  props: {
    position: Object
  },
  data() {
    return {
      fields: {
        title: { value: this.position.title, errors: [] }
      },
      inProgress: false,
      rules: {
        required: validators.required('Обязательное поле.'),
      },

    }
  },
  methods: {
    async update() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await positionsApi().update(this.position.uuid, formData)
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