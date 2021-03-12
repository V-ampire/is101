import statuses from "@/core/services/statuses";


export default {
  methods: {
    getStatusClasses (item) {
      if (item.status == statuses.archived) {
        return 'archive'
      }
    },
  },
}