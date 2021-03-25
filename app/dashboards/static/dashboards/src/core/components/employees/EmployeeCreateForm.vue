<template>
  <v-form ref="form">
    <div class="form-fields d-flex flex-column mb-3">
      <div class="username-field">
        <div class="username-field-label subtitle-2 mb-2">Логин для входа в систему</div>
        <div class="username-field-input">
          <v-text-field
            v-model="fields.username.value"
            :error-messages="fields.username.errors"
            :rules="[rules.required, rules.min]"
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
						:rules="[rules.required, rules.emailMatch]"
						label="Имеил"
            name="email"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="password-field">
        <div class="password-field-label subtitle-2 mb-2">Пароль</div>
        <div class="password-field-input">
          <v-text-field
            v-model="fields.password.value"
            :error-messages="fields.password.errors"
            :append-icon="showPassword ? 'fa-eye' : 'fa-eye-slash'"
            :rules="[rules.required, rules.min, rules.passwordMatch]"
            :type="showPassword ? 'text' : 'password'"
            name="password"
            hint="Минимум 8 символов"
            label="Пароль"
            counter
            @click:append="showPassword = !showPassword"
          ></v-text-field>
        </div>
        <div class="password-field-btn-generate">
          <v-btn
            x-small
            block
            color="primary"
            @click="genSafePassword()"
          >Создать надежный пароль
          </v-btn>
        </div>
      </div>
      <div class="fio-field">
        <div class="fio-field-label subtitle-2 mb-2">ФИО работника</div>
        <div class="fio-field-input">
          <v-text-field
						v-model="fields.fio.value"
						:error-messages="fields.fio.errors"
						:rules="[rules.required]"
						label="ФИО работника"
            name="fio"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="position-field">
        <div class="position-field-label subtitle-2 mb-2">Должность</div>
        <div class="position-field-input">
          <v-select
            v-model="fields.position.value"
            :error-messages="fields.position.errors"
            :items="positionItems"
            item-text="title"
            item-value="uuid"
          ></v-select>
        </div>
      </div>
      <div class="date_of_birth-field">
        <div class="date_of_birth-field-label subtitle-2 mb-2">Дата рождения</div>
        <div class="date_of_birth-field-input">
          <v-menu
            ref="menu"
            v-model="dateOfBirthMenu"
            :close-on-content-click="false"
            :return-value.sync="date"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="fields.date_of_birth.value"
                :error-messages="fields.date_of_birth.errors"
                label="Дата рождения"
                prepend-icon="fa-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="fields.date_of_birth.value"
              no-title
              scrollable
            >
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                @click="menu = false"
              >
                Закрыть
              </v-btn>
              <v-btn
                text
                color="primary"
                @click="$refs.menu.save(date)"
              >
                OK
              </v-btn>
            </v-date-picker>
          </v-menu>
        </div>
      </div>
      <div class="pasport-field">
        <div class="pasport-field-label subtitle-2 mb-2">Паспортные данные</div>
        <div class="pasport-field-input">
          <v-text-field
						v-model="fields.pasport.value"
						:error-messages="fields.pasport.errors"
						:rules="[rules.required]"
						label="Паспортные данные"
            name="pasport"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="pasport_scan-field">
        <div class="pasport_scan-field-label subtitle-2 mb-2">Скан паспорта</div>
        <div class="pasport_scan-field-input">
          <v-file-input
						v-model="fields.pasport_scan.value"
						:error-messages="fields.pasport_scan.errors"
						accept=".jpeg, .jpg, .pdf, .zip"
						label="Скан паспорта"
            name="pasport_scan"
            :rules="[rules.required]"
					></v-file-input>
        </div>
      </div>
    </div>
    <div class="form-btn mb-3">
      <FormButton
        label="Создать работника"
        :inProgress="inProgress"
        @onAction="create()"
      ></FormButton>
    </div>
    <div class="form-message">
      <v-alert
        v-if="!!successHtml"
        dense
        text
        type="success"
        v-html="successHtml"
      ></v-alert>
    </div>
  </v-form>
</template>


<script>
import createFormMixin from '@/core/mixins/createFormMixin';
import eventUtils from '@/core/services/events/utils';
import validators from '@/core/validators';
import { employeesApi, positionsApi } from '@/core/services/http/clients';
import FormButton from '@/core/components/commons/FormButton';
import { generatePassword } from '@/core/services/accounts/utils';

export default {
  mixins: [createFormMixin],
  components: {
    FormButton: FormButton
  },
  props: {
    companyUuid: String,
    branchUuid: String
  },
  data() {
    return {
      fields: {
        username: { value: '', errors: [] },
        password: { value: '', errors: [] },
        email: { value: '', errors: [] },
        fio: { value: '', errors: [] },
        position: { value: '', errors: [] },
        date_of_birth: { value: '', errors: [] },
        pasport: { value: '', errors: [] },
        pasport_scan: { value: '', errors: [] },
      },
      rules: {
        required: validators.required('Обязательное поле.'),
        emailMatch: validators.emailMatch('Не валидный имеил.'),
        passwordMatch: validators.regexpMatch(
          /(?=.*[0-9])(?=.*[a-zA-Z])/,
          'Пароль должен содержать цифры и буквы.'
        ),
        min: validators.minLength(8, 'Минимальная длина 8 символов.'),
      },
      showPassword: false,
      positionList: [],
      dateOfBirthMenu: false,
    }
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    },
    positionItems() {
      let items = [];
      for (let position of this.positionList) {
        items.push({
          title: position.title,
          uuid: position.uuid,
        })
      }
      return items
    }
  },
  async mounted() {
    this.positionList = await this.getPositions();
  },
  methods: {
    async getPositions() {
      let response;
      try {
        response = await positionsApi().list('works')
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (Array.isArray(response.data)) {
        return response.data
      } else {
        const errorMessage = 'Не удалось загрузить список должностей.';
        eventUtils.showErrorAlert(errorMessage);
        console.log(`Не удалось загрузить список должностей. Получен ответ ${response}`);
      }
    },
    afterCreate(employeeData) {
      const route = this.$router.resolve({
        name: 'EmployeeDetail', 
        params: { 
          companyUuid: this.companyUuid, 
          branchUuid: this.branchUuid, 
          employeeUuid: employeeData.uuid
        }
      });
      this.successHtml = `
        Работник <a href="${route.href}">${employeeData.fio}</a> успешно создан.`;
    },
    genSafePassword() {
      const password = generatePassword();
      this.fields.password.value = password;
      this.showPassword = true;
    },
  },
}
</script>