<template>
    <v-dialog
    v-model="dialog"
    max-width="900px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="primary"
                v-bind="attrs"
                v-on="on"
            >Добавить</v-btn>
        </template>
        <v-card class="pb-4">
            <v-card-title class="headline">Добавить Юр. лицо</v-card-title>
            <v-card-text>
                <user-form ref="createUserForm"></user-form>
                <v-divider class="mx-4"></v-divider>
                <company-form ref="createCompanyForm"></company-form>
            </v-card-text>
            <v-card-actions>
                <v-btn
                    color="primary"
                    @click="createCompany"
                >Добавить</v-btn>
                <v-btn
                    color="primary"
                    @click="closeDialog"
                >Отмена</v-btn>
                <v-progress-linear
                    :active="loading"
                    :indeterminate="loading"
                    absolute
                    bottom
                    color="deep-purple accent-4"
                ></v-progress-linear>
                <v-alert v-show="created.status=='success'" type="success">
                    {{ created.message }}
                </v-alert>
                <v-alert v-show="created.status=='error'" type="error">
                    {{ created.message }}
                </v-alert>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import CompanyForm from '@/components/CompanyForm'
import UserForm from '@/components/CreateUserForm'
import api from '@/services/companies/ApiClient'

    export default {
        data: () => ({
            dialog: false,
            loading: false,
            created: {
                status: '',
                message: ''
            }
        }),
        computed: {
            userData: function() {
                return this.$refs.createUserForm.getAsObject()
            },
            companyData: function() {
                return this.$refs.createCompanyForm.getAsFormData()
            }
        },
        components: {
            'company-form': CompanyForm,
            'user-form': UserForm
        },
        methods: {
            createCompany: function() {
                if (this._validateForms()) {
                    this.loading = true;
                    const data = this.companyData;
                    data.append('user.username', this.userData.username);
                    data.append('user.password', this.userData.password);
                    api.create(data).then(res => {
                        console.log(res.data);
                        console.log(res)
                        this.loading = false;
                    });
                }
            },
            closeDialog: function() {
                this.created = {
                    status: '',
                    message: ''
                };
                this.dialog = false;
            },
            _validateForms() {
                return this.$refs.createUserForm.validate() && this.$refs.createCompanyForm.validate()
            }
        },
    }
</script>