<template>
  <v-form ref="form">
    <div class="form-fields d-flex flex-column mb-3">
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
        <div class="address-field-label subtitle-2 mb-2">Адрес филиала, без города</div>
        <div class="address-field-input">
          <v-text-field
            v-model="fields.address.value"
            :error-messages="fields.address.errors"
            :rules="[rules.required]"
            label="Адрес, без города"
            name="address"
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
        label="Создать филиал"
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
import { branchesApi } from '@/core/services/http/clients';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [createFormMixin],
  components: {
    FormButton: FormButton
  },
  props: {
    companyUuid: String
  },
  data() {
    return {
      fields: {
        city: { value: '', errors: [] },
        address: { value: '', errors: [] },
        phone: { value: '', errors: [] },
      },
      rules: {
        required: validators.required('Обязательное поле.'),
      },
    }
  },
  computed: {
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  methods: {
    afterCreate(branchData) {
      const route = this.$router.resolve({
        name: 'BranchDetail', params: { companyUuid: this.companyUuid, branchUuid: branchData.uuid }
      });
      this.successHtml = `
        Филиал <a href="${route.href}">${branchData.address}</a> успешно создан.`;
    },
  }
}
</script>