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
                <v-alert v-html="alerts.success.message" v-show="alerts.success.show" type="success">
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
import api from '@/services/companies/Client'

    export default {
        data: () => {
            return {
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
            }
        },
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
                this.clearAlerts();
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
                            this.onError(error);
                        }
                    )
                }
            },
            closeDialog: function() {
                this.dialog = false;
                this.clearAlerts();
            },
            validateForms: function() {
                return this.$refs.createUserForm.validate() && this.$refs.createCompanyForm.validate()
            },
            onCreated: function(company) {
                // При успешном добавлении вызвать событие ос статусом создания
                // Вывести информацию о новом объекте
                this.alerts.success.show = true;
                this.alerts.success.message = `Юр.лицо <a href="${company.url}">${company.title}</a> добавлено.`;
                this.$emit(this.createdEvent, this.succesStatus);
            },
            onError: function(error) {
                // При ошибке вызвать событие со статусом ошибки
                // Вывести информацию об ошибке
                // Обработать ошибку
                let errorDetails;
                if (error.response) {
                    errorDetails = this.processServerError(error);
                } else if (error.request) {
                    errorDetails = this.processRequestError(error);
                } else {
                    errorDetails = this.processSettingRequestError(error);
                }
                this.alerts.error.show = true;
                this.alerts.error.message = errorDetails.message;
                console.log(errorDetails);
                this.$emit(
                    this.createdEvent,
                    {
                        status: this.errorStatus,
                        details: errorDetails
                    }
                );
            },
            processServerError: function(error) {
                // Обработка ошибки сервера
                let errorDetails = {
                    errorInfo: {
                        response: error.response
                    },
                    message: 'Сервер вернул ошибку! Повторите попытку чуть позже...'
                };
                const errorData = error.response.data;
                if (error.response.status == 400) {
                    for (let field in errorData) {
                        if (field == 'user') {
                            for (let message of errorData[field]) {
                                this.$refs.createUserForm.setErrorMessage('username', message);
                            }
                        }
                        if (this.$refs.createCompanyForm.fields[field] !== undefined) {
                            for (let message of errorData[field]) {
                                this.$refs.createCompanyForm.setErrorMessage(field, message);
                            }
                        }
                    }
                    errorDetails.message = 'Ошибка! Проверьте правильность заполнение полей форм!';
                }
                return errorDetails
                
            },
            processRequestError: function(error) {
                // Обработка ошибки клиента при отправлении запроса
                return {
                    errorInfo: {
                        request: error.request,
                    },
                    message: 'Упс! Возникла ошибка, возможно, нет соединения с интернетом...'
                }
            },
            processSettingRequestError: function(error) {
                // Обработка ошибки клиента при инициировании запроса
                return {
                    errorInfo: {
                        message: error.message,
                    },
                    message: 'Упс! Возникла какая то ошибка, повторите попытку чуть позже...'
                }
            },
            clearAlerts: function() {
                this.alerts.success.show = false;
                this.alerts.success.message = '';
                this.alerts.error.show = false;
                this.alerts.error.message = '';
            }
        },
    }
</script>