<template>
<div>
    <v-list>
        <v-list-item v-for="company in companies" :key="company.title">
            <v-flex>
                <a :href=company.url>
                    <span>{{company.title}}</span>
                </a>
                <span>{{ company.city }}</span>
            </v-flex>
        </v-list-item>
    </v-list>
</div>
</template>


<script>
import companyApi from '@/services/CompanyApi'

export default {
    data() {
        return {
            companies: []
        }
    },
    mounted() {
        companyApi.fetchCompanyList()
            .then(companies => {
                this.companies = companies
            })
            .catch(error => {
                console.log(error)
            })

    }
}
</script>
