<template>
  <v-form ref="form">
    <div class="form-fields d-flex flex-column mb-3">
      <div class="username-field">
        <div class="username-field-label subtitle-2 mb-2">Логин для входа в систему</div>
        <div class="username-field-input">
          <v-text-field
            v-model="fields.username.value"
            :error-messages="fields.username.errors"
            :rules="[rules.min]"
            label="Логин"
            name="username"
            counter
          ></v-text-field>
        </div>
      </div>
      <div class="email-field">
        <div class="email-field-label subtitle-2 mb-2">E-mail</div>
        <div class="email-field-input">
          <v-text-field
						v-model="fields.email.value"
						:error-messages="fields.email.errors"
						:rules="[rules.emailMatch]"
						label="Имеил"
            name="email"
						counter
					></v-text-field>
        </div>
      </div>
    </div>
    <div class="form-btn mb-3">
      <FormButton
        label="Создать юрлицо"
        :inProgress="inProgress"
        @onAction="update()"
      ></FormButton>
    </div>

  </v-form>
</template>

<script>
import { companyAccountsApi, employeeAccountsApi } from '@/core/services/http/clients';
import roles from '@/core/services/roles';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import validators from '@/core/validators';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [formFieldsMixin],
  components: {
    FormButton: FormButton,
  },
  props: {
    accountUuid: String,
    accountRole: String
  },
  data() {
    return {
      fields: {
        username: { value: '', errors: [] },
        email: { value: '', errors: [] },
      },
      rules: {
        min: validators.minLength(8, 'Минимальная длина 8 символов.'),
        emailMatch: validators.emailMatch('Не валидный имеил.')
      },
      inProgress: false
    }
  },
  computed: {
    api() {
      if (this.accountRole === roles.company[0]) {
        return companyAccountsApi()
      } else if (this.accountRole === roles.employee[0]) {
        return employeeAccountsApi()
      }
    }
  },
  methods: {
    update() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await this.api.update(this.accountUuid, formData);
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
        eventUtils.showSuccessEvent('Данные обновлены.');
      }
    }
  },
}
</script>