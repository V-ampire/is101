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
      </div>
      <div class="title-field">
        <div class="title-field-label subtitle-2 mb-2">Название компании</div>
        <div class="title-field-input">
          <v-text-field
						v-model="fields.title.value"
						:error-messages="fields.title.errors"
						:rules="[rules.required]"
						label="Название компании"
            name="title"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="logo-field">
        <div class="logo-field-label subtitle-2 mb-2">Логотип компании</div>
        <div class="logo-field-input">
          <v-file-input
						v-model="fields.logo.value"
						:error-messages="fields.logo.errors"
						accept=".jpeg, .jpg, .png"
						label="Логотип компании"
            name="logo"
            :rules="[rules.required]"
					></v-file-input>
        </div>
      </div>
      <div class="tagline-field">
        <div class="tagline-field-label subtitle-2 mb-2">Слоган компании</div>
        <div class="tagline-field-input">
          <v-text-field
						v-model="fields.tagline.value"
						:error-messages="fields.tagline.errors"
						:rules="[rules.required]"
						label="Слоган"
            name="tagline"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="inn-field">
        <div class="inn-field-label subtitle-2 mb-2">ИНН компании</div>
        <div class="inn-field-input">
          <v-text-field
						v-model="fields.inn.value"
						:error-messages="fields.inn.errors"
						:rules="[rules.required]"
						label="ИНН"
            name="inn"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="ogrn-field">
        <div class="ogrn-field-label subtitle-2 mb-2">ОГРН/ОГРНИП компании</div>
        <div class="ogrn-field-input">
          <v-text-field
						v-model="fields.ogrn.value"
						:error-messages="fields.ogrn.errors"
						:rules="[rules.required]"
						label="ОГРН"
            name="ogrn"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="city-field">
        <div class="city-field-label subtitle-2 mb-2">Город</div>
        <div class="city-field-input">
          <v-text-field
						v-model="fields.city.value"
						:error-messages="fields.city.errors"
						:rules="[rules.required]"
						label="Город"
            name="city"
						counter
					></v-text-field>
        </div>
      </div>
      <div class="address-field">
        <div class="address-field-label subtitle-2 mb-2">Адрес (без города)</div>
        <div class="address-field-input">
          <v-text-field
						v-model="fields.address.value"
						:error-messages="fields.address.errors"
						:rules="[rules.required]"
						label="Адрес"
            name="address"
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
      <div class="phone-field">
        <div class="phone-field-label subtitle-2 mb-2">Телефон</div>
        <div class="phone-field-input">
          <v-text-field
						v-model="fields.phone.value"
						:error-messages="fields.phone.errors"
						:rules="[rules.required]"
						label="Телефон"
            name="phone"
						counter
					></v-text-field>
        </div>
      </div>
    </div>
    <div class="form-btn mb-3">
      <FormButton
        label="Создать юрлицо"
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
import validators from '@/core/validators';
import { companiesApi } from '@/core/services/http/clients';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [createFormMixin],
  components: {
    FormButton: FormButton
  },
  data () {
    return {
      fields: {
        username: { value: '', errors: [] },
        password: { value: '', errors: [] },
        title: { value: '', errors: [] },
        logo: { value: null, errors: [] },
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
        emailMatch: validators.emailMatch('Не валидный имеил.'),
        passwordMatch: validators.regexpMatch(
          /(?=.*[0-9])(?=.*[a-zA-Z])/,
          'Пароль должен содержать цифры и буквы.'
        ),
        min: validators.minLength(8, 'Минимальная длина 8 символов.'),
      },
      showPassword: false,
    }
  },
  computed: {
    api() {
      return companiesApi()
    }
  },
  methods: {
    afterCreate(companyData) {
      /**
       * Устанавливает сообщение об успешном создании.
       * @companyData - данные созданной компании
       */
      // Создать html со ссылкой на новое юрлицо
      const route = this.$router.resolve({
        name: 'CompanyDetail', params: { companyUuid: companyData.uuid }
      });
      this.successHtml = `
        Юрлицо <a href="${route.href}">${companyData.title}</a> успешно создано.`;
    },
  }
}
</script>
