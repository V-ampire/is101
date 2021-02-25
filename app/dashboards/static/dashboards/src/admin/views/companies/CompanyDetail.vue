<template>
  <div>
    Hello Company Detail!
  </div>
</template>

<script>
import companiesApi from "@/core/services/http/companies";
// import statuses from "@/core/services/statuses";
// import utils from '@/core/services/events/utils';
import { processHttpError } from '@/core/services/errors/utils';

export default {
  data () {
    return {
      companyInfo: {}
    }
  },
  computed: {
    companyUuid() {
      return this.$route.params.companyUuid;
    }
  },
  mounted() {
    this.getCompanyInfo();
  },
  methods: {
    async getCompanyInfo() {
      let response;
      try {
        response = await companiesApi.detail(this.companyUuid);
      } catch (err) {
        return processHttpError(err);
      }
      const companyData = response.data;
      console.log(companyData)
    }
  },
}
</script>