<template>
  <v-form ref="form">
    <div v-if="!!fields.title" class="title-field d-flex flex-column mb-3">
      <div class="title-field-label subtitle-2 mb-2">Название компании</div>
      <div class="title-field-input">
        <v-text-field
          v-model="fields.title.value"
          :error-messages="fields.title.errors"
          label="Название компании"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.logo" class="logo-field d-flex flex-column">
      <div class="logo-field-label subtitle-2 mb-2">
        Логотип компании
      </div>
      <div v-if="!!fields.logo.value" class="logo-field-preview">
        <v-img 
          :src="fields.logo.value"
          max-height="280"
        ></v-img>
      </div>
      <div class="logo-field-input">
        <v-file-input
          prepend-icon="fa-camera"
          v-model="fields.logo.value"
          :error-messages="fields.logo.errors"
          accept=".jpeg, .jpg, .png"
          ></v-file-input>
        <div class="logo-field-input-help caption">
          Изображение должно быть в формате 'jpeg', 'jpg' или 'png'
        </div>
      </div>
    </div>
    <div v-if="!!fields.tagline" class="tagline-field d-flex flex-column mb-3">
      <div class="tagline-field-label subtitle-2 mb-2">Слоган компании</div>
      <div class="tagline-field-input">
        <v-text-field
          v-model="fields.tagline.value"
          :error-messages="fields.tagline.errors"
          label="Слоган компании"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.inn" class="inn-field d-flex flex-column mb-3">
      <div class="inn-field-label subtitle-2 mb-2">ИНН компании</div>
      <div class="inn-field-input">
        <v-text-field
          v-model="fields.inn.value"
          :error-messages="fields.inn.errors"
          label="ИНН компании"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.ogrn" class="ogrn-field d-flex flex-column mb-3">
      <div class="ogrn-field-label subtitle-2 mb-2">ОГРН\ОГРНИП компании</div>
      <div class="ogrn-field-input">
        <v-text-field
          v-model="fields.ogrn.value"
          :error-messages="fields.ogrn.errors"
          label="ОГРН\ОГРНИП компании"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.city" class="city-field d-flex flex-column mb-3">
      <div class="city-field-label subtitle-2 mb-2">Город</div>
      <div class="city-field-input">
        <v-text-field
          v-model="fields.city.value"
          :error-messages="fields.city.errors"
          label="Город"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.address" class="address-field d-flex flex-column mb-3">
      <div class="address-field-label subtitle-2 mb-2">Адрес, без города</div>
      <div class="address-field-input">
        <v-text-field
          v-model="fields.address.value"
          :error-messages="fields.address.errors"
          label="Адрес, без города"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.email" class="email-field d-flex flex-column mb-3">
      <div class="email-field-label subtitle-2 mb-2">E-mail</div>
      <div class="email-field-input">
        <v-text-field
          v-model="fields.email.value"
          :rules="[rules.emailMatch]"
          :error-messages="fields.email.errors"
          label="E-mail"
        ></v-text-field>
      </div>
    </div>
    <div v-if="!!fields.phone" class="phone-field d-flex flex-column mb-3">
      <div class="phone-field-label subtitle-2 mb-2">Телефон</div>
      <div class="phone-field-input">
        <v-text-field
          v-model="fields.phone.value"
          :error-messages="fields.phone.errors"
          label="Телефон"
        ></v-text-field>
      </div>
    </div>
    <div class="form-btn">
      <FormButton 
        @onAction="updateCompanyInfo()"
        label="Обновить информацию"
      ></FormButton>
    </div>
  </v-form>
</template>

<script>
import validators from '@/core/validators';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import CompanyApi from '@/core/services/http/companies';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [formFieldsMixin],
  components: {
    FormButton: FormButton
  },
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
      },
      inProgress: false,
    }
  },
  props: {
    companyUuid: String
  },
  mounted() {
    this.setInitial(this.initialData);
  },
  methods: {
    testButton() {
      console.log(this.fields.title.value);
    },
    async updateCompanyInfo() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await CompanyApi.update(this.companyUuid, formData)
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
        eventUtils.showSuccessEvent('Данные изменены!');
      }
    },
    cleanFields(formFields) {
      // Если лого не файл - удалить из полей.
      if (!(formFields.logo instanceof File)) {
        delete formFields.logo;
      }
      return formFields
    }
  },
}
</script>
