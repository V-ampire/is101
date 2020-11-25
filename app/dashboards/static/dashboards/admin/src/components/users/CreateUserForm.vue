<template>
    <v-form ref="form">
        <v-container>
            <v-row>
                <v-col cols="12">Создать учетную запись для юр. лица</v-col>
                <v-col cols="12">
                    <v-text-field
                        v-model="fields.username.value"
                        :error-messages="fields.username.error"
                        :rules="[rules.required, rules.min]"
                        label="Логин"
                        counter
                        required
                    ></v-text-field>
                </v-col>
                <v-col cols="12">
                    <v-text-field
                        v-model="fields.password.value"
                        :error-messages="fields.password.error"
                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required, rules.min, rules.passwordMatch]"
                        :type="showPassword ? 'text' : 'password'"
                        name="input-10-1"
                        hint="At least 8 characters"
                        label="Пароль"
                        counter
                        @click:append="showPassword = !showPassword"
                    >
                    </v-text-field>
                </v-col>
                <v-col cols="12">
                    <v-btn
                        small
                        color="primary"
                        @click="generatePassword"
                    >Создать надежный пароль
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>


<script>
import passwordGen from 'password-generator'
import validators from '@/validators';
import formDataMixin from '@/components/mixins/formDataMixin';

export default {
    mixins: [formDataMixin],
    data () {
        return {
            fields: {
                username: {
                    value: '',
                    error: ''
                },
                password: {
                    value: '',
                    error: ''
                }
            },
            showPassword: false,
            rules: {
                required: validators.required('Обязательное поле.'),
                min: validators.minLength(6, 'Минимальная длина 8 символов.'),
                passwordMatch: validators.regexpMatch(
                    /(?=.*[0-9])(?=.*[a-zA-Z])/,
                    'Пароль должен содержать цифры и буквы.'
                )
            }
        }   
    },
    methods: {
        generatePassword: function() {
            const pattern = /(?=.*[0-9])(?=.*[a-zA-Z!@#$%^&*])/;
            let password = passwordGen(
                8, 
                false, 
                /[\d\W\w\p]/
            );
            while (!pattern.test(password)) {
                password = passwordGen(
                    8, 
                    false, 
                    /[\d\W\w\p]/
                );
            }
            this.fields.password.value = password;
            this.showPassword = true;
        },
    },
}
</script>