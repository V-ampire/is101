<template>
	<v-form>
		<v-card>
			<v-card-title>
				Создать учетную запись для юр. лица
			</v-card-title>
			<v-card-text>
				<v-text-field
		            v-model="username"
		            :rules="nameRules"
		            label="Логин"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="password"
		            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
		            :rules="[rules.required, rules.min]"
		            :type="show1 ? 'text' : 'password'"
		            name="input-10-1"
		            hint="At least 8 characters"
		            label="Пароль"
		            counter
		            @click:append="show1 = !show1"
	          	></v-text-field>
			</v-card-text>
		</v-card>
		<v-card>
			<v-card-title>
				Данные юридического лица
			</v-card-title>
			<v-card-text>
				<v-text-field
		            v-model="title"
		            :rules="nameRules"
		            label="Название компании"
		            counter
		            required
	          	></v-text-field>
	          	<v-file-input
				    accept=".jpeg, .jpg, .png"
				    label="Логотип компании"
				></v-file-input>
				<v-text-field
		            v-model="tagline"
		            :rules="nameRules"
		            label="Слоган"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="inn"
		            :rules="nameRules"
		            label="ИНН"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="ogrn"
		            :rules="nameRules"
		            label="ОГРН"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="city"
		            :rules="nameRules"
		            label="Город"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="address"
		            :rules="nameRules"
		            label="Адрес"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="email"
		            :rules="nameRules"
		            label="Имеил"
		            counter
		            required
	          	></v-text-field>
	          	<v-text-field
		            v-model="phone"
		            :rules="nameRules"
		            label="Телефон"
		            counter
		            required
	          	></v-text-field>
			</v-card-text>
		</v-card>
	</v-form>
</template>


<script>
	export default {
		data () {
			return {
		        show1: false,
		        username: '',
		        password: 'Password',
		        title: '',
		        logo: '',
		        tagline: '',
		        inn: '',
		        ogrn: '',
		        city: '',
		        address: '',
		        email: '',
		        phone: '',
		        rules: {
			        required: value => !!value || 'Required.',
			        min: v => v.length >= 8 || 'Min 8 characters',
			        emailMatch: () => (`The email and password you entered don't match`),
		        }
			}
      	}
	}
</script>