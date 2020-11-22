<template>
    <v-container>
        <v-card>
            <v-card-title>Юридические лица</v-card-title>
            <v-container>
                <v-row>
                    <v-col cols="8">
                        <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Поиск"
                        single-line
                        hide-details
                        ></v-text-field>
                    </v-col>
                    <v-col cols="4">
                        <v-card-actions>
                            <add-dialog></add-dialog>
                        </v-card-actions>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <v-data-table
                        :headers="headers"
                        :items="companies"
                        :search="search"
                        :item-class="getRowClasses"
                        :sort-by="status"
                        >
                            <template v-slot:item.actions="{ item }">
                                <v-icon 
                                v-if="item.status==1" 
                                small 
                                class="mr-2" 
                                @click="editCompany(item.uuid)">
                                mdi-pencil</v-icon>
                                <v-icon 
                                v-if="item.status==1" 
                                small
                                @click="deleteCompany(item.uuid)">
                                mdi-delete</v-icon>
                            </template>
                            <template v-slot:item.title="{ item }">
                                <a v-if="item.status==1" href="#">{{ item.title }}</a>
                                <span v-else>{{ item.title }}</span>
                            </template>
                        </v-data-table>
                    </v-col>
                </v-row>
            </v-container>
        </v-card>
    </v-container>
</template>


<script>
import CreateCompanyDialog from '@/components/CreateCompanyDialog'
import api from '@/services/companies/ApiClient'

export default {
    data() {
        return {
            headers: [
                {text: 'Название юр. лица', value: 'title'},
                {text: 'Город', value: 'city' },
                {text: 'Адрес', value: 'address' },
                {text: 'Статус', value: 'status' },
                {text: 'Действия', value: 'actions', sortable: false}
            ],
            companies: [],
            search: '',
            statuses: {
                active: 1,
                archive: 0
            }
        }
    },
    components: {
        'add-dialog': CreateCompanyDialog
    },
    mounted() {
        api.fetchAll()
            .then(companies => {
                this.companies = companies
            })
            .catch(error => {
                console.log(error)
            })
    },
    methods: {
        editCompany: function(company_uuid) {
            console.log(company_uuid);
            this.companies.unshift({
                title: 'New',
                city: 'New',
                address: 'new',
                status: 1
            })
        },

        deleteCompany: function(company_uuid) {
            console.log(`Delete company ${company_uuid}`);
        },
        getRowClasses: function(item) {
            if (item.status == this.statuses.archive) {
                return 'archive'
            }
        }
    }
}
</script>

