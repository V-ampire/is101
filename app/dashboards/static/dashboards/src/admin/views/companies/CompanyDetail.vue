<template>
  <div>
    Hello Company Detail!
  </div>
</template>

<script>
export default {
  data () {
    return {

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
    getCompanyInfo() {
      console.log(this.companyUuid);
    }
  },
}
</script>