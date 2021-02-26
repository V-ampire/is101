<template>
  <v-form>
    <div class="logo-field d-flex">
    <div v-if="!!fields.logo.value" class="logo-field-preview">
      <v-img src="fields.logo.value"></v-img>
    </div>
    <v-file-input
      v-model="fields.logo.value"
      :error-messages="fields.logo.errors"
      accept=".jpeg, .jpg, .png"
      label="Логотип компании"
    ></v-file-input>
    </div>

  </v-form>
</template>

<script>
import validators from '@/core/validators'
import formDataMixin from '@/core/mixins/formDataMixin'

export default {
  mixins: [formDataMixin],
  data () {
    return {
      fields: {
        title: { value: '', errors: [] },
        logo: { value: '', errors: [] },
        tagline: { value: '', errors: [] },
        inn: { value: '', errors: [] },
        ogrn: { value: '', errors: [] },
        city: { value: '', errors: [] },
        address: { value: '', errors: [] },
        email: { value: '', errors: [] },
        phone: { value: '', errors: [] },
      },
      rules: {
        required: validators.required('Обязательное поле.'),
        emailMatch: validators.emailMatch('Не валидный имеил.')
      }
    }
  },
  props: {
    initial: Object
  },
  mounted () {
    this.fromInitial(this.initial)
    console.log(this.initial)
  },
}
</script>
