<template>
  <v-form ref="form">
    <div class="form-fields">
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
        <div class="pasport_scan-field-label subtitle-2">Скан паспорта</div>
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
        <div v-if="!!passportScanDownload" class="pasport_scan-field-download caption">
          <a :href="passportScanDownload" download>{{ fields.pasport_scan.value }}</a>
        </div>
      </div>
    </div>
    <div class="form-btn">
      <FormButton 
        @onAction="update()"
        :inProgress="inProgress"
        label="Обновить информацию"
      ></FormButton>
    </div>
  </v-form>
</template>


<script>
import validators from '@/core/validators';
import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import { employeesApi } from '@/core/services/http/clients';
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
    branchUuid: String,
    employeeUuid: String
  },
  data() {
    return {
      fields: {
        fio: { value: '', errors: [] },
        date_of_birth: { value: '', errors: [] },
        pasport: { value: '', errors: [] },
        pasport_scan: { value: '', errors: [] },
      },
      rules: {
        required: validators.required('Обязательное поле.'),
      },
      positionList: [],
      dateOfBirthMenu: false,
    }
  },
  computed: {
    api() {
      return employeesApi(this.companyUuid, this.branchUuid)
    },
    passportScanDownload() {
      const currentValue = this.fields.pasport_scan.value;
      if (currentValue && typeof currentValue === 'string') {
        return currentValue
      } else {
        return null
      }
    }
  },
  methods: {
    async update() {
      if (this.validate()) {
        this.inProgress = true;
        const formData = this.getAsFormData();
        try {
          await this.api.update(this.employeeUuid, formData)
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
      // Если скан не файл - удалить из полей.
      if (!(formFields.pasport_scan instanceof File)) {
        delete formFields.pasport_scan;
      }
      return formFields
    }
  },
}
</script>