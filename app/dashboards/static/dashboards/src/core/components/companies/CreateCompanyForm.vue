<template>
	<v-form ref="form">
		<v-container>
			<v-row>
				<v-col cols="12">Данные юридического лица</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.title.value"
						:error-messages="fields.title.errors"
						:rules="[rules.required]"
						label="Название компании"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-file-input
						v-model="fields.logo.value"
						:error-messages="fields.logo.errors"
						accept=".jpeg, .jpg, .png"
						label="Логотип компании"
					></v-file-input>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.tagline.value"
						:error-messages="fields.tagline.errors"
						:rules="[rules.required]"
						label="Слоган"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.inn.value"
						:error-messages="fields.inn.errors"
						:rules="[rules.required]"
						label="ИНН"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.ogrn.value"
						:error-messages="fields.ogrn.errors"
						:rules="[rules.required]"
						label="ОГРН"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.city.value"
						:error-messages="fields.city.errors"
						:rules="[rules.required]"
						label="Город"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.address.value"
						:error-messages="fields.address.errors"
						:rules="[rules.required]"
						label="Адрес"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.email.value"
						:error-messages="fields.email.errors"
						:rules="[rules.required, rules.emailMatch]"
						label="Имеил"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="fields.phone.value"
						:error-messages="fields.phone.errors"
						:rules="[rules.required]"
						label="Телефон"
						counter
					></v-text-field>
				</v-col>
			</v-row>
		</v-container>
	</v-form>
</template>


<script>
	import validators from '@/core/validators'
	import formDataMixin from '@/core/mixins/formDataMixin'

	export default {
		mixins: [formDataMixin],
		data () {
			return {
				fields: {
					title: {
						value: '',
						errors: []
					},
					logo: {
						value: '',
						errors: []
					},
					tagline: {
						value: '',
						errors: []
					},
					inn: {
						value: '',
						errors: []
					},
					ogrn: {
						value: '',
						errors: []
					},
					city: {
						value: '',
						errors: []
					},
					address: {
						value: '',
						errors: []
					},
					email: {
						value: '',
						errors: []
					},
					phone: {
						value: '',
						errors: []
					},
				},
				rules: {
					required: validators.required('Обязательное поле.'),
					emailMatch: validators.emailMatch('Не валидный имеил.')
				}
			}
		},
	}
</script>