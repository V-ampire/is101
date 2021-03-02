<template>
  <v-form ref="form">
    <div class="fields d-flex flex-column">
      <div class="isActive-field mb-4">
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
        <v-divider></v-divider>
      </div>
      <div class="enter-field">
        <div class="enter-field-label subtitle-2 mb-2">Данные для входа:</div>
        <div class="enter-field-username mb-3">
          <v-text-field
            v-model="fields.username.value"
            :error-messages="fields.username.errors"
            :rules="[rules.required, rules.min]"
            label="Логин"
            counter
            required
          ></v-text-field>
        </div>
        <div class="enter-field-btn d-flex flex-sm-column">
          <v-btn
            class="mr-3"
            small
            color="primary" 
            @click="updateUsername()"
          >
            Обновить логин
          </v-btn>
          <v-dialog
            v-model="passwordDialog"
            persistent
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn 
                color="primary"
                small
              >
                Изменить пароль
              </v-btn>
            </template>
            <v-card>
              <v-card-title>Изменить пароль</v-card-title>
            </v-card>
        </div>
      </div>
    </div>
  </v-form>
</template>


<script>
import validators from '@/core/validators';
import formDataMixin from '@/core/mixins/formDataMixin';
import accountsApi from '@/core/services/http/accounts';
import eventUtils from '@/core/services/events/utils';
import errorUtils from '@/core/services/errors/utils';


export default {
    mixins: [formDataMixin],
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
          min: validators.minLength(6, 'Минимальная длина 8 символов.'),
        },
      }   
    },
    methods: {
      async switchIsActive () {
        this.isActiveInProgress = true;
        let response;
        console.log(this.fields.is_active.value);
        try {
          if (this.fields.is_active.value) {
          // Разблокировать
            response = await accountsApi.companies.activate(this.accountUuid);
          } else {
            // Заблокировать
            response = await accountsApi.companies.deactivate(this.accountUuid);
          }
        } catch (err) {
          this.fields.is_active.value = !this.fields.is_active.value; // Отменить изменение поля
          const httpError = errorUtils.checkHttpError(err);
          eventUtils.showErrorAlert(httpError.message);
          this.isActiveInProgress = false;
          throw err
        }
        this.isActiveInProgress = false;
      },
      async updateUsername() {
        let response;
        const formData = this.getAsFormData(['username']);
        try {
            response = await accountsApi.companies.update(this.accountUuid, formData);
          } catch (err) {
            const httpError = errorUtils.checkHttpError(err);
            eventUtils.showErrorAlert(httpError.message);
            throw err
        }
      }
    },
}
</script>