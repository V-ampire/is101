<template>
    <v-container>
        <v-list
            v-for="company in companies"
            :key="company.uuid">
            <company-item
                uuid=company.uuid,
                url=company.url,
                city=company.city,
                title=company.title,
                status=company.status
            ></company-item>
        </v-list>
    </v-container>
</template>


<script>
import CompanyListItem from './CompanyListItem'
import companyApi from '@/services/CompanyApi'

export default {
    data() {
        return {
            companies: []
        }
    },
    components: {
        'company-item': CompanyListItem
    },
    mounted() {
        companyApi.fetchAll()
            .then(companies => {
                this.companies = companies
            })
            .catch(error => {
                console.log(error)
            })

    }
}
</script>
