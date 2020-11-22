<template>
    <v-form ref="form">
        <v-container>
            <v-row>
                <v-col cols="12">Создать учетную запись для юр. лица</v-col>
                <v-col cols="12">
                    <v-text-field
                        v-model="username"
                        :rules="[rules.required, rules.min]"
                        label="Логин"
                        counter
                        required
                    ></v-text-field>
                </v-col>
                <v-col cols="12">
                    <v-text-field
                        v-model="password"
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

export default {
    data () {
        return {
            username: '',
            password: '',
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
        getFormData: function() {
            return {
                username: this.username,
                password: this.password
            }
        },
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
            this.password = password
            this.showPassword = true;
        },
        validate() {
            return this.$refs.form.validate();
        }
    },
}
</script>