<template>
  <v-dialog
    v-model="dialog"
    max-width="900px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="primary"
        v-bind="attrs"
        v-on="on"
      >Добавить юр. лицо</v-btn>
    </template>
    <v-card class="pb-4">
      <v-card-title class="headline">Добавить Юр. лицо</v-card-title>
        <v-card-text>
          <UserForm ref="createUserForm"/>
          <v-divider class="mx-4"></v-divider>
          <CompanyForm ref="createCompanyForm"/>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="primary"
              @click="createCompany"
          >Добавить юр. лицо</v-btn>
          <v-btn
            color="primary"
            @click="closeDialog"
          >Отмена</v-btn>
          <v-progress-linear
            :active="loading"
            :indeterminate="loading"
            absolute
            bottom
            color="deep-purple accent-4"
          ></v-progress-linear>
        </v-card-actions>
        <div class="status-alert">
          <v-alert v-html="alerts.success.message" v-show="alerts.success.show" type="success">
          </v-alert>
          <v-alert v-show="alerts.error.show" type="error">
              {{ alerts.error.message }}
          </v-alert>
        </div>
    </v-card>
  </v-dialog>
</template>


<script>
import setErrorMixin from '@/core/mixins/setErrorMixin'
import CompanyForm from '@/core/components/companies/CompanyForm'
import UserForm from '@/core/components/users/UserForm'
import api from '@/core/services/http/companies'
import {processHttpError} from '@/core/services/http/utils'

export default {
  mixins: [setErrorMixin],
  data () {
    return {
      dialog: false,
      loading: false,
      alerts: {
        success: {
            show: false,
            message: ''
        },
        error: {
            show: false,
            message: ''
        }
      }
    }
  },
  components: {
    CompanyForm,
    UserForm,
  },
  computed: {
    userData () {
      return this.$refs.createUserForm.getAsObject()
    },
    companyFormData () {
      return this.$refs.createCompanyForm.getAsFormData()
    }
  },
  methods: {
    closeDialog () {
      this.dialog = false;
      this.clearAlerts();
    },
    clearAlerts () {
      this.alerts.success.show = false;
      this.alerts.success.message = '';
      this.alerts.error.show = false;
      this.alerts.error.message = '';
    },
    validateForms: function() {
      return this.$refs.createUserForm.validate() && this.$refs.createCompanyForm.validate()
    },
    createCompany () {
      // Проверит валидность форм
      // Отправить запрос на создание юрлица
      // Вызвать метод обработки результата
      this.clearAlerts();
      if (this.validateForms()) {
        this.loading = true;
        const data = this.companyFormData;
        data.append('user.username', this.userData.username);
        data.append('user.password', this.userData.password);
        api.create(data)
          .then(response => {
              this.loading = false;
              this.onCreated(response.data);
          })
          .catch(error => {
              this.loading = false;
              this.onError(error);
          })
      }
    },
    onCreated (company) {
      // Вывести информацию о новом объекте
      this.alerts.success.show = true;
      this.alerts.success.message = `Юр.лицо <a href="${company.url}">${company.title}</a> добавлено.`;
    },
    onError (error) {
      let message = 'Упс! Возникла какая то ошибка, повторите попытку чуть позже...';
      try {
        processHttpError(error);
      } catch(e) {
        // Если неверно заполнена форма то отобразить ошибку на форме
        if (e.name == 'ServerError') {
          if (error.response.status == 400) {
            this.setComponentError(error)
            return
          }
        }
        message = e.message;
      }
      // Иначе показать глобальный алерт с ошибкой
      this.setAppError({message: message})
    },
    setComponentError (error) {
      const errorData = error.response.data;
      for (let field of Object.keys(errorData)) {
        if (field == 'user') {
          for (let message of errorData[field]) {
            this.$refs.createUserForm.setErrorMessage('username', message);
          }
        }
        if (this.$refs.createCompanyForm.fields[field] !== undefined) {
          for (let message of errorData[field]) {
            this.$refs.createCompanyForm.setErrorMessage(field, message);
          }
        }
      }
      this.alerts.error.show = true;
      this.alerts.error.message = 'Ошибка! Проверьте правильность заполнение полей форм!';
    }
  },
}
</script>