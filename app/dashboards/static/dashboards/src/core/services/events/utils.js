import { ON_APP_ERROR, ON_OPEN_CONFIRM, ON_CONFIRM_RESULT } from '@/core/services/events/types'
import eventBus from '@/core/services/events/eventBus'

export default {
  showErrorAlert(errorMessage) {
    /**
     * Показать окно с ошибкой.
     * @errorMessage - сообщение об ошибке
     */
    eventBus.$emit(ON_APP_ERROR, errorMessage);
  },
  onErrorEvent(handler) {
    /**
     * Вклюить обработку ошибок.
     * @handler - обработчик в который будет передано сообщение об ошибке.
     */
    eventBus.$on(ON_APP_ERROR, handler);
  },
  onConfirmAction(confirmParams, action) {
    /**
     * Установить обработчик события подтверждения.
     * После подтверждения удаляет обработчик.
     * @action - Колбек, который нужно выполнить при подтверждении, в колбек будет
     * передан результат подтверждения.
     * Вызвать событие для открытия окна подтверждения.
     */
    eventBus.$on(ON_CONFIRM_RESULT, (result) => {
      eventBus.$off(ON_CONFIRM_RESULT);
      action(result);
    })
    eventBus.$emit(ON_OPEN_CONFIRM, confirmParams);
  },
  onOpenConfirmAction(handler) {
    /**
     * Включает обработку события на открытие окна подтверждения.
     */
    eventBus.$on(ON_OPEN_CONFIRM, handler);
  },
  confirmAction(result) {
    /**
     * Вызывает событие подтверждения действия с результатом подтверждения.
     * @result - рзультат подтверждения действия.
     */
    eventBus.$emit(ON_CONFIRM_RESULT, result);
  }
}