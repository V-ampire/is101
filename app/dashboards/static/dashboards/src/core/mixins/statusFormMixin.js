/**
 * Миксин для форм изменеия статуса.
 */
export default {
  props: {
    currentStatus: String,
    objectUuid: String
  },
  data() {
    return {
      endpoint: ''
    }
  },
}