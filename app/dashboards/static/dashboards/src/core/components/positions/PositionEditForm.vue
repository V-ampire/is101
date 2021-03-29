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
      console.log(this.getAsObject())
    }
  },
}
</script>