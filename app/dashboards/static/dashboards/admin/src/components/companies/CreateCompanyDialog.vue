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
            </v-card-actions>
            <div class="status-alert">
                <v-alert v-show="alerts.success.show" type="success">
                    {{ alerts.success.message }}
                </v-alert>
                <v-alert v-show="alerts.error.show" type="error">
                    {{ alerts.error.message }}
                </v-alert>
            </div>
        </v-card>
    </v-dialog>
</template>

<script>
    /*
Диалог для создания нового юрлица.
Генерирует событие:
companyCreated - в случает успешного создания юрлица, возвращает статус запроса created/error
*/
import CompanyForm from '@/components/companies/CompanyForm'
import UserForm from '@/components/users/CreateUserForm'
import api from '@/services/companies/ApiClient'

    export default {
        data: () => ({
            dialog: false,
            loading: false,
            createdEvent: 'companyCreated',
            succesStatus: 'created',
            errorStatus: 'error',
            alerts: {
                success: {
                    show: false,
                    message: ''
                },
                error: {
                    show: false,
                    message: ''
                }
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
                // Проверит валидность форм
                // Отправить запрос на создание юрлица
                // Вызвать метод обработки результата
                if (this.validateForms()) {
                    this.loading = true;
                    const data = this.companyData;
                    data.append('user.username', this.userData.username);
                    data.append('user.password', this.userData.password);
                    api.create(data)
                        .then(response => {
                            this.loading = false;
                            this.onCreated(response.data);
                        })
                        .catch(error => {
                            this.loading = false;
                            // if (error.response) {
                            //     this.$emit(this.createdEvent, this.errorStatus);
                            // } else if (error.request) {
                            //     // The request was made but no response was received
                            //     // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                            //     // http.ClientRequest in node.js

                            //     this.$emit(this.createdEvent, {status: 'error', data: 'Упс! Возникла ошибка, возможно, нет соединения с интернетом...'});
                            //     console.log(error.request);
                            // } else {
                            //     // Something happened in setting up the request that triggered an Error
                            //     this.$emit(this.events.failCreated, {status: 'error', data: 'Упс! Возникла какая то ошибка, повторите попытку чуть позже...'});
                            //     console.log('Error', error.message);
                            this.onError(error);
                        }
                    )
                }
            },
            closeDialog: function() {
                this.dialog = false;
            },
            validateForms: function() {
                return this.$refs.createUserForm.validate() && this.$refs.createCompanyForm.validate()
            },
            onCreated: function(company) {
                // При успешном добавлении вызвать событие ос статусом создания
                // Вывести информацию о новом объекте
                this.$emit(this.createdEvent, this.succesStatus);
                this.alerts.success.show = true;
                this.alerts.success.message = `Юр.лицо <a href="${company.url}">${company.title}</a> добавлено.`;
            },
            onError: function(error) {
                // При ошибке вызвать событие со статусом ошибки
                // Вывести информацию об ошибке
                // Обработать ошибку
                this.$emit(this.createdEvent, this.errorStatus);
                if (error.response) {
                    const errorData = error.response.data;
                    if (error.response.status == 400) {
                        for (let field in errorData) {
                            if (field == 'user') {
                                for (let message in errorData[field]) {
                                    this.$refs.createUserForm.setErrorMessage('username', message);
                                }
                            }
                            console.log(this.$refs.createCompanyForm.fields);
                            if (this.$refs.createCompanyForm.fields.includes(field)) {
                                for (let message in errorData[field]) {
                                    this.$refs.createUserForm.setErrorMessage('username', message);
                                }
                            }
                        }
                        this.alerts.error.show = true;
                        this.alerts.error.message = 'Ошибка! Проверьте правильность заполнение полей форм!';
                    }
                }
            }
        },
    }
</script>