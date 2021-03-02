<template>
  <v-form ref="changePasswordForm">
    <div class="d-flex flex-column form-fields">
      <v-text-field
        v-model="fields.password1.value"
        :error-messages="fields.password1.errors"
        :append-icon="showPassword ? 'fa-eye' : 'fa-eye-slash'"
        :rules="[rules.required, rules.min, rules.passwordMatch]"
        :type="showPassword ? 'text' : 'password'"
        name="password1"
        hint="At least 8 characters"
        label="Пароль"
        counter
        @click:append="showPassword = !showPassword"
      ></v-text-field>
      <v-text-field
        v-model="fields.password2.value"
        :error-messages="fields.password2.errors"
        :append-icon="showPassword ? 'fa-eye' : 'fa-eye-slash'"
        :rules="[rules.required, rules.min, rules.passwordMatch]"
        :type="showPassword ? 'text' : 'password'"
        name="password2"
        hint="At least 8 characters"
        label="Подтвердите пароль"
        counter
        @click:append="showPassword = !showPassword"
      ></v-text-field>
      <v-btn 
        color="primary"
        small
        @click="changePassword()"
      >
        Изменить пароль
      </v-btn>
    </div>
  </v-form>
</template>


<script>
import validators from '@/core/validators';
import formDataMixin from '@/core/mixins/formDataMixin';


export default {
  mixins: [formDataMixin],
  props: {
    accountUuid: String
  },
  data () {
    return {
      fields: {
        password1: {
          value: '',
          errors: []
        },
        password2: {
          value: '',
          errors: []
        },
      },
      showPassword: false,
      rules: {
        required: validators.required('Обязательное поле.'),
        min: validators.minLength(6, 'Минимальная длина 8 символов.'),
        passwordMatch: validators.regexpMatch(
            /(?=.*[0-9])(?=.*[a-zA-Z])/,
            'Пароль должен содержать цифры и буквы.'
        )
      }
    }
  },
  methods: {
    async changePassword () {
      let response;
      const formData = this.getAsFormData();
      try {
          response = await accountsApi.companies.changePassword(this.accountUuid, formData);
      } catch (err) {
        const httpError = errorUtils.checkHttpError(err);
        eventUtils.showErrorAlert(httpError.message);
        throw err
      }
    }
  },
}
</script>