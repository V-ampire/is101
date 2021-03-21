from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers


class UserAccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учетной записи.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'uuid', 'password', 'is_active')
        reda_only_fields = ('is_active',)

    def create(self, validated_data):
        raise NotImplementedError('Define wchich user role to use for creating.')

    def validate_password(self, password_value):
        """
        При попытке обновить пароль выдаем ошибку, т.к. для смены пароля используется
        специальное действие.
        """
        if self.instance:
            raise serializers.ValidationError("Для изменения пароля используйте функцию сброса пароля")
        password_validation.validate_password(password_value)
        return password_value


class CompanyUserAccountSerializer(UserAccountSerializer):
    """
    Сериалайзер для учетной записи юр. лица.
    """
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        return get_user_model().company_objects.create_user(username, email, password)


class EmployeeUserAccountSerializer(UserAccountSerializer):
    """
    Сериалайзер для учетной записи работника.
    """
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        return get_user_model().employee_objects.create_user(username, email, password)
    
    
class ReadOnlyUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'uuid', 'role', 'is_active')
        read_only_fields = ('username', 'email', 'uuid', 'role', 'is_active')


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