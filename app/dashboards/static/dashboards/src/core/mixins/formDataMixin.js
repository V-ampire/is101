/*
Миксин для работы с Vuetify формами.
Для использования в данных компонента определить параметр fields в виде объекта
fields: {
    fieldName: {
        value: '',
        error: ''
    },
    ...
}
Определяет методы:
    setInitial(initialData) - заполняет поля формы начальными данными,
      ключи initialData будут сооinitialDataтветствовать названием полей, причем поазаны будут лишь те поля
      ключи для которых присутствуют в initialData
    getAsFormData(fields) - возвращает данные формы в виде объекта FormData
    getAsObject(fields)   - возвращает данные формы в виде обычного js Object
    setErrorMessage(ieldName, errorMessage) - устанавливает значение prop error-messages для поля fieldName
*/

export default {
    data () {
      return {
        fields: null,
        initialData: null,
      }
    },
    methods: {
        getAsFormData (fields=[]) {
            const formData = new FormData();
            const useFields = (fields.length > 0) ? fields : Object.keys(this.fields);
            for (let field of useFields) {
              console.log(field);
              console.log(this.fields);
              formData.append(field, this.fields[field].value);
            }
            return formData
        },
        getAsObject (fields=[]) {
            const formData = {};
            const useFields = (fields.length > 0) ? fields : Object.keys(this.fields);
            for (let field of useFields) {
                formData[field] = this.fields[field].value;
            }
            return formData
        },
        setErrorMessage (fieldName, errorMessage) {
            console.log(fieldName);
            console.log(errorMessage);
            this.fields[fieldName].errors.push(errorMessage);
        },
        setInitial (initialData) {
          /**
           * Устанавливает в свойство this.fields.value начальные данные
           * @initialFields - начальный данные
           */
          this.initialData = initialData;
          for (let key in initialData) {
            if (key in this.fields) {
              this.fields[key].value = initialData[key]
            }
          }
        },
        validate () {
            return this.$refs.form.validate();
        },
    }
}