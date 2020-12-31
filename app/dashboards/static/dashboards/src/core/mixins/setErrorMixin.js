import { NotImplementedError } from '@/core/errors'
import { ON_APP_ERROR } from '@/core/events/types'
import eventBus from '@/core/events/eventBus'

export default {
  // Миксин содержащий методы для обработки ошибок
  methods: {
    setComponentError () {
      // Обработка ошибки на компоненте, например валидация формы
      throw NotImplementedError('Метод не реализован!')
    },
    setAppError (errorData) {
      // Ошибка будет обработана на уровне приложения, через событие
      eventBus.$emit(ON_APP_ERROR, errorData)
    }
  },
}