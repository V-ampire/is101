from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers


class CompanyUserAccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учетной записи юр. лица.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'uuid', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        return get_user_model().company_objects.create_account(username, password)

    def validate_password(self, password_value):
        """
        При попытке обновить пароль выдаем ошибку, т.к. для смены пароля используется
        специальное действие.
        """
        if self.instance:
            raise serializers.ValidationError(
                "Для изменения пароля используйте функцию сброса пароля"
            )
        return password_value


class ReadOnlyCompanyUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'uuid')
        read_only_fields = ('username', 'uuid')


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    def validate_password1(self, password1_value):
        password_validation.validate_password(password1_value)
        return password1_value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают!')
        return data