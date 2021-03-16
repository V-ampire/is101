<template>
  <v-form ref="form">
    <div class="fields d-flex flex-column">
      <div v-if="!!fields.is_active" class="isActive-field mb-4">
        <div class="isActive-field-label subtitle-2">Доступ в систему:</div>
        <div class="isActive-field-switch">
          <v-switch
            v-model="fields.is_active.value"
            :label="fields.is_active.value ? 'Доступ разрешен' : 'Доступ ограничен'"
            @change="switchIsActive"
          >
            <template v-slot:label>
              <span v-if="isActiveInProgress">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </span>
              <span class="green--text ml-2" v-else-if="fields.is_active.value">
                <v-icon color="green">fa-check-circle</v-icon> Доступ разрешен
              </span>
              <span class="red--text ml-2" v-else>
                <v-icon color="red">fa-times-circle</v-icon> Доступ ограничен
              </span>
            </template>
          </v-switch>
        </div>
      </div>
      <v-divider></v-divider>
      <div class="enter-fields d-flex flex-column">
        <div v-if="!!fields.username" class="username-field mb-3">
          <div class="username-field-label subtitle-2 mb-2">Данные для входа:</div>
          <div class="username-field-input mb-2">
            <v-text-field
              v-model="fields.username.value"
              :error-messages="fields.username.errors"
              :rules="[rules.required, rules.min]"
              label="Логин"
              counter
              required
            ></v-text-field>
          </div>
          <div class="username-field-btn">
            <FormButton
            label="Обновить логин"
              @onAction="updateUsername()"
            ></FormButton>
          </div>
        </div>
        <div class="password-field">
          <v-dialog
            v-model="passwordDialog"
            max-width="360"
          >
            <template v-slot:activator="{ on, attrs }">
              <div class="password-field-btn">
                <v-btn
                  color="primary"
                  small
                  block
                  v-bind="attrs"
                  v-on="on"
                >
                  Изменить пароль
                </v-btn>
              </div>
            </template>
            <v-card>
              <v-card-title>Изменить пароль</v-card-title>
              <v-card-text>
                <ChangePasswordForm
                  :accountUuid="accountUuid"
                ></ChangePasswordForm>
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>
      </div>
    </div>
  </v-form>
</template>


<script>
import validators from '@/core/validators';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import accountsApi from '@/core/services/http/accounts';
import eventUtils from '@/core/services/events/utils';
import ChangePasswordForm from '@/core/components/accounts/ChangePasswordForm';
import FormButton from '@/core/components/commons/FormButton';
import { ServerError } from '@/core/services/errors/types';

export default {
    mixins: [formFieldsMixin],
    components: {
      FormButton: FormButton,
      ChangePasswordForm: ChangePasswordForm
    },
    props: {
      accountUuid: String
    },
    data () {
      return {
        fields: {
          username: {
            value: '',
            errors: []
          },
          is_active: {
            value: false,
            errors: []
          }
        },
        isActiveInProgress: false,
        passwordDialog: false,
        rules: {
          required: validators.required('Обязательное поле.'),
          min: validators.minLength(8, 'Минимальная длина 8 символов.'),
        },
      }   
    },
    mounted() {
      this.setInitial(this.initialData);
    },
    methods: {
      async switchIsActive () {
        this.isActiveInProgress = true;
        try {
          if (this.fields.is_active.value) {
          // Разблокировать
            await accountsApi.companies.activate(this.accountUuid);
          } else {
            // Заблокировать
            await accountsApi.companies.deactivate(this.accountUuid);
          }
        } catch (err) {
          this.fields.is_active.value = !this.fields.is_active.value; // Отменить изменение поля
          eventUtils.showErrorAlert(err.message);
          this.isActiveInProgress = false;
          throw err
        }
        this.isActiveInProgress = false;
      },
      async updateUsername() {
        if (this.validate()) {
          const formData = this.getAsFormData(['username']);
          try {
            await accountsApi.companies.update(this.accountUuid, formData);
          } catch (err) {
            if (err instanceof ServerError && !!err.data.username) {
              this.setErrorMessages('username', err.data.username)
            } else {
              eventUtils.showErrorAlert(err.message);
            }
            throw err
          }
          eventUtils.showSuccessEvent('Логин обновлен!');
          eventUtils.reloadData();
        }
      }
    },
}
</script>