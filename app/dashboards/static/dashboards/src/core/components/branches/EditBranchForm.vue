<template>
  <v-form ref="form">
    <div class="city-field d-flex flex-column mb-3">
      <div class="city-field-label subtitle-2 mb-2">Город</div>
      <div class="city-field-input">
        <v-text-field
          v-model="fields.city.value"
          :error-messages="fields.city.errors"
          label="Город"
        ></v-text-field>
      </div>
    </div>
    <div class="address-field d-flex flex-column mb-3">
      <div class="address-field-label subtitle-2 mb-2">Адрес, без города</div>
      <div class="address-field-input">
        <v-text-field
          v-model="fields.address.value"
          :error-messages="fields.address.errors"
          label="Адрес, без города"
        ></v-text-field>
      </div>
    </div>
    <div class="phone-field d-flex flex-column mb-3">
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
        @onAction="updateBranchInfo()"
        label="Обновить информацию"
      ></FormButton>
    </div>
  </v-form>
</template>


<script>
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import {branchesApi} from '@/core/services/http/clients';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';
import FormButton from '@/core/components/commons/FormButton';

export default {
  mixins: [formFieldsMixin],
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
        city: { value: '', errors: [] },
        address: { value: '', errors: [] },
        phone: { value: '', errors: [] }
      },
    }
  },
  computed: {
    api() {
      return branchesApi(this.companyUuid) 
    }
  },
  methods: {
    async updateBranchInfo() {
      if (this.validate()) {
        const formData = this.getAsFormData();
        try {
          await this.api.update(this.branchUuid, formData)
        } catch (err) {
          if (err instanceof ServerError) {
            for (let field of Object.keys(err.data)) {
              this.setErrorMessages(field, err.data[field])
            }
          } else {
            eventUtils.showErrorAlert(err.message);
          }
          throw err
        }
        eventUtils.showSuccessEvent('Данные изменены!');
      }
    }
  }

}
</script>
