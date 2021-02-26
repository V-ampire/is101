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
    fromInitial(initialData) - заполняет поля формы начальными данными,
      ключи initialData будут сооinitialDataтветствовать названием полей, причем поазаны будут лишь те поля
      ключи для которых присутствуют в initialData
    getAsFormData() - возвращает данные формы в виде объекта FormData
    getAsObject()   - возвращает данные формы в виде обычного js Object
    setErrorMessage(ieldName, errorMessage) - устанавливает значение prop error-messages для поля fieldName
*/

export default {
    data () {
      return {
        fields: {}
      }
    },
    methods: {
        getAsFormData () {
            const formData = new FormData();
            for (let field in this.fields) {
                formData.append(field, this.fields[field].value);
            }
            return formData
        },
        getAsObject () {
            const formData = {};
            for (let field in this.fields) {
                formData[field] = this.fields[field].value;
            }
            return formData
        },
        setErrorMessage (fieldName, errorMessage) {
            console.log(fieldName);
            console.log(errorMessage);
            this.fields[fieldName].errors.push(errorMessage);
        },
        fromInitial (initialData) {
          /**
           * Устанавливает в свойство this.fields.value начальные данные
           * @initialFields - начальный данные
           */
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