<template>
	<v-form ref="form">
		<v-container>
			<v-row>
				<v-col cols="12">Данные юридического лица</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="title"
						:rules="[rules.required]"
						label="Название компании"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-file-input
						v-model="logo"
						accept=".jpeg, .jpg, .png"
						label="Логотип компании"
					></v-file-input>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="tagline"
						:rules="[rules.required]"
						label="Слоган"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="inn"
						:rules="[rules.required]"
						label="ИНН"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="ogrn"
						:rules="[rules.required]"
						label="ОГРН"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="city"
						:rules="[rules.required]"
						label="Город"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="address"
						:rules="[rules.required]"
						label="Адрес"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="email"
						:rules="[rules.required, rules.emailMatch]"
						label="Имеил"
						counter
					></v-text-field>
				</v-col>
				<v-col cols="12">
					<v-text-field
						v-model="phone"
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
	import validators from '@/validators';
	import formDataMixin from '@/components/mixins/formDataMixin';

	export default {
		mixins: [formDataMixin],
		data () {
			return {
				fields: {
					title: {
						value: '',
						error: ''
					},
					logo: {
						value: '',
						error: ''
					},
					tagline: {
						value: '',
						error: ''
					},
					inn: {
						value: '',
						error: ''
					},
					ogrn: {
						value: '',
						error: ''
					},
					city: {
						value: '',
						error: ''
					},
					address: {
						value: '',
						error: ''
					},
					email: {
						value: '',
						error: ''
					},
					phone: {
						value: '',
						error: ''
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