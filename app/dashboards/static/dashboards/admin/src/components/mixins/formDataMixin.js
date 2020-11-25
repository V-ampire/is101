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
    getAsFormData() - возвращает данные формы в виде объекта FormData
    getAsObject()   - возвращает данные формы в виде обычного js Object
    setErrorMessage(fieldName) - устанавливает значение prop error-messages для поля fieldName
*/

export default {
    methods: {
        getAsFormData: function() {
            const formData = new FormData();
            for (let field in this.fields) {
                formData.append(field, this.fields[field].value);
            }
            return formData
        },
        getAsObject: function() {
            const formData = {};
            for (let field in this.fields) {
                formData[field] = this.fields[field].value;
            }
            return formData
        },
        setErrorMessage: function(fieldName, errorMessage) {
            this.fields[fieldName].errors.push(errorMessage);
        },
        validate: function() {
            return this.$refs.form.validate();
        },
        computed: {
            fields: function() {
                return Object.keys(Object.assign({}, ...this.fields))
            }
        },
    },
}