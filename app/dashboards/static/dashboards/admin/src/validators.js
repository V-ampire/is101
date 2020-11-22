// Валидация значений полей форм и т.п.


export default {
    required: function(message) {
        /*
        Проверка на истинность значения.
        :param message: - сообщение, если не пройдена валидация. Если не задано вернет false.
        Возвращает функцию, принимающую проверяемое значение.
        Например:
        
        const validate = minLength(2, 'Обязательное поле');
        validate('Значение') // true
        validate('') // Обязательное поле
        */
       return function(value) {
            if (!value) {
                return message || false
            }
            return true
        }
    },

    minLength(length, message) {
        /*
        Проверка на минимальную длину
        :param length: минимальная длина
        :param message: - сообщение, если не пройдена валидация. Если не задано вернет false.
        Возвращает функцию, принимающую проверяемое значение.
        Например:
        
        const min = minLength(2, 'Минимум 2 символа.');
        min('12') // true
        min('1') // Минимум 2 символа
        */
        return function(value) {
            if (value.length <= length) {
                return message || false
            }
            return true
        }
    },

    maxLength(length, message) {
        /*
        Проверка на максимальную длину
        :param length: минимальная длина
        :param message: - сообщение, если не пройдена валидация. Если не задано вернет false.
        Возвращает функцию, принимающую проверяемое значение.
        Например:
        
        const max = maxLength(3, 'Максимум 2 символа.');
        max('12') // true
        max('123') // Максимум 2 символа
        */
        return function(value) {
            if (value.length > length) {
                return message || false
            }
            return true
        }
    },

    emailMatch(message) {
        /*
        Валидация email.
        :param message: - сообщение, если не пройдена валидация. Если не задано вернет false.
        Возвращает функцию, принимающую проверяемое значение.
        */
        return function(value) {
            const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if (!pattern.test(value)) {
                return message || false
            }
            return true
        }
    },

    regexpMatch(pattern, message) {
        /*
        Проверка на соответствие регулярному выражению.
        :param message: - сообщение, если не пройдена валидация. Если не задано вернет false.
        Возвращает функцию, принимающую проверяемое значение.
        */
        return function(value) {
            if (!pattern.test(value)) {
                return message || false
            }
            return true
        }
    }
}