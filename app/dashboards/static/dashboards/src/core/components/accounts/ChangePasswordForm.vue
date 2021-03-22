<template>
  <v-form ref="form">
    <div class="d-flex flex-column form-fields">
      <div class="password1-field">
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
      </div>
      <div class="password2-field">
        <v-text-field
          v-model="fields.password2.value"
          :error-messages="fields.password2.errors"
          :append-icon="showPassword ? 'fa-eye' : 'fa-eye-slash'"
          :rules="[rules.required, rules.min, rules.passwordMatch, checkPassword2]"
          :type="showPassword ? 'text' : 'password'"
          name="password2"
          hint="At least 8 characters"
          label="Подтвердите пароль"
          counter
          @click:append="showPassword = !showPassword"
        ></v-text-field>
      </div>
      <div class="form-btn">
        <div class="form-btn-change mb-3">
          <FormButton
            label="Изменить пароль"
            :inProgress="inProgress"
            @onAction="changePassword()"
          ></FormButton>
        </div>
        <div class="form-btn-generate">
          <v-btn
            small
            block
            color="primary"
            @click="genSafePassword()"
          >Создать надежный пароль
          </v-btn>
        </div>
      </div>
    </div>
  </v-form>
</template>


<script>
import validators from '@/core/validators';
import { generatePassword } from '@/core/services/accounts/utils';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import accountsApiMixin from '@/core/mixins/accountsApiMixin';
import FormButton from '@/core/components/commons/FormButton';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';

export default {
  mixins: [formFieldsMixin, accountsApiMixin],
  components: {
    FormButton: FormButton
  },
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
      inProgress: false,
      rules: {
        required: validators.required('Обязательное поле.'),
        min: validators.minLength(6, 'Минимальная длина 8 символов.'),
        passwordMatch: validators.regexpMatch(
            /(?=.*[0-9])(?=.*[a-zA-Z])/,
            'Пароль должен содержать цифры и буквы.'
        ),
      }
    }
  },
  methods: {
    async changePassword () {
      if(this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await this.api.changePassword(this.accountUuid, formData);
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
        this.showPassword = false;
        eventUtils.showSuccessEvent('Пароль изменен!');
      }
    },
    genSafePassword() {
      const password = generatePassword();
      this.fields.password1.value = password;
      this.showPassword = true;
    },
    checkPassword2(password2) {
      const message = 'Пароли не совпадают.';
      const password1 = this.fields.password1.value;
        return (password1 === password2) ? true : message
  }
  },
}
</script>