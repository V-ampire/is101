/**
 * Миксин для форм создания новытьх объектов. Наслеуется от formFieldsMixin
 * Для использования необходимо:
 *  - определить computed свойство api, которое возвращает клиент для обращения к API.
 *  - привязать к кнопке создания объекта метод create()
 * Миксин предоставляет метод afterCreate(createdObjectData), который выполняется после создания
 * объекта. В нем можно определить любые необходиме действия.
 * После создания будет вызвано событие onReload
 */

import formFieldsMixin from '@/core/mixins/formFieldsMixin';
import eventUtils from '@/core/services/events/utils';
import { ServerError } from '@/core/services/errors/types';
import { ON_RELOAD } from '@/core/services/events/types';

export default {
  mixins: [formFieldsMixin],
  data() {
    return {
      successHtml: null,
      inProgress: false
    }
  },
  methods: {
    async create () {
      this.inProgress = true;
      let response;
      if (this.validate()) {
        const formData = this.getAsFormData();
        try {
          response = await this.api.create(formData);
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
        this.afterCreate(response.data);
        this.$emit(ON_RELOAD);
      }
    },
    afterCreate(data) {
      /**
       * Определите любые необходимые действия после создания объекта.
       */
      return data
    },
    reset() {
      this.$refs.form.reset();
      this.successHtml = null;
    }
  }
}