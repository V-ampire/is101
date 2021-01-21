from rest_framework.serializers import ValidationError

from api.v1.accounts import serializers

from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestUserAccountSerializer():

    def setup_method(self, method):
        self.serializer_class = serializers.UserAccountSerializer

    def test_validate_password_error(self, company_user):
        tested_password = fake.password()
        serializer = self.serializer_class(company_user)
        expected_message = "Для изменения пароля используйте функцию сброса пароля"

        with pytest.raises(ValidationError) as e:
            exc_info = e
            serializer.validate_password(tested_password)
        assert exc_info.value.args[0] == expected_message

    def test_validate_password_success(self, company_user):
        tested_password = fake.password()
        serializer = self.serializer_class()
        expected_message = "Для изменения пароля используйте функцию сброса пароля"

        assert serializer.validate_password(tested_password) == tested_password


@pytest.mark.django_db
class TestChangePasswordSerializer():

    def setup_method(self, method):
        self.serializer_class = serializers.ChangePasswordSerializer
    
    def test_validate_password1(self, mocker):
        mock_validate = mocker.patch('api.v1.accounts.serializers.password_validation.validate_password')
        expected_password = fake.password()
        serializer = self.serializer_class()
        validated_password = serializer.validate_password1(expected_password)

        assert validated_password == expected_password
        mock_validate.assert_called_with(expected_password)

    def validate_error(self):
        expected_password1 = fake.password()
        expected_password2 = fake.password()
        data = {
            'password1': expected_password1,
            'password2': expected_password2
        }
        expected_msg = 'Пароли не совпадают!'
        serializer = self.serializer_class()
        with pytest.raises(ValidationError) as e:
            exc_info = e
            serializer.validate_password(tested_password)
        assert exc_info.value.args[0] == expected_message

    def validate_success(self):
        expected_password1 = fake.password()
        expected_password2 = expected_password1
        expected_data = {
            'password1': expected_password1,
            'password2': expected_password2
        }
        serializer = self.serializer_class()
        validated_data = serializer.validate(expected_data)

        assert validated_data == expected_data