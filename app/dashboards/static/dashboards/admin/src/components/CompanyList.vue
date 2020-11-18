<template>
    <v-container>
        <v-data-table
            :headers="headers"
            :items="companies"
        ></v-data-table>
    </v-container>
</template>


<script>
import companyApi from '@/services/CompanyApi'

export default {
    data() {
        return {
            headers: [
                {
                    text: 'Название юр. лица',
                    value: 'title',
                },
                {
                    text: 'Город',
                    value: 'city'
                },
                {
                    text: 'Адрес',
                    value: 'address'
                },
                {
                    text: 'Статус',
                    value: 'status'
                }
            ],
            companies: []
        }
    },
    computed: {
        companyLink: function()
    }
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
