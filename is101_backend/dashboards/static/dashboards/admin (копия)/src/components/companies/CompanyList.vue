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
                            <create-dialog v-on:companyCreated="processCreate"></create-dialog>
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
import CreateCompanyDialog from '@/components/companies/CreateCompanyDialog'
import api from '@/services/companies/Client'
import EventBus from '@/eventBus'
import {processError, HttpError} from "@/errors/http"

export default {
    data () {
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
        'create-dialog': CreateCompanyDialog
    },
    mounted() {
        this.getCompanies();
    },
    methods: {
        getCompanyByUUID: function(company_uuid) {
            for (let company of this.companies) {
                if (company.uuid == company_uuid) {
                    return company
                }
            }
        },
        getCompanies: function() {
            api.getAll()
                .then(companies => {
                    this.companies = companies
                })
                .catch(error => {
                    try {
                        processError(error)
                    } catch (err) {
                        if (err instanceof HttpError) {
                            EventBus.$emit('OPEN_STATUS_ALERT', {
                                status: 'error',
                                message: err.message
                            })
                        }
                    }
                    
                })
        },
        editCompany: function(company_uuid) {
            this.companies.unshift({
                title: 'New',
                city: 'New',
                address: 'new',
                status: 1
            })
        },
        deleteCompany: function(company_uuid) {
            var self = this;
            const params = {
                description: `Удалить юр. лицо ${this.getCompanyByUUID(company_uuid).title}`,
                action: (params) => {
                    api.delete(params.company_uuid)
                        .then(response => {
                            self.refreshTable();
                        })
                        .catch(error => {
                            console.log(error);
                        })
                    
                },
                actionParams: {company_uuid: company_uuid}
            };
            EventBus.$emit('OPEN_CONFIRM', params);
        },
        getRowClasses: function(item) {
            if (item.status == this.statuses.archive) {
                return 'archive'
            }
        },
        refreshTable: function() {
            this.getCompanies();
        },
        processCreate: function(response) {
            if (response.status == 'success') {
                this.refreshTable();
            } else {
                console.log(response.data);
            }
        }
    }
}
</script>

