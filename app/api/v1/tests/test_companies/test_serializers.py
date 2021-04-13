from rest_framework.serializers import ValidationError as APIValidationError

from api.v1.companies import serializers

from accounts.factories import CompanyUserAccountModelFactory, AdminUserAccountModelFactory

from companies.factories import CompanyProfileFactory
from companies.models import CompanyProfile

from factory_generator import generate_to_dict
from faker import Faker
import pytest
from unittest.mock import Mock


fake = Faker()


@pytest.mark.django_db
class TestCompanyCreateSerializer():

    def setup_method(self, method):
        self.user = CompanyUserAccountModelFactory.create()
        self.create_data = generate_to_dict(CompanyProfileFactory)
        self.create_data.pop('user')
        self.create_data['username'] = f'{fake.user_name()}@{fake.user_name()}'
        self.create_data['password'] = fake.password()
        self.create_data['email'] = fake.email()
        self.serializer_class = serializers.CompanyCreateSerializer
        self.request = Mock(user=self.user)

    def test_validate_user_data(self, mocker):
        mock_validate_user = mocker.patch(
            'api.v1.companies.serializers.CompanyUserAccountSerializer.is_valid'
        )
        serializer = self.serializer_class()
        serializer.validate(self.create_data)
        mock_validate_user.assert_called_with(raise_exception=True)
    
    def test_create_company(self, mocker):
        mock_create = mocker.patch('api.v1.companies.serializers.utils.create_company')
        expected_company = mocker.Mock()
        mock_create.return_value = expected_company
        expected_data = self.create_data.copy()
        expected_username = expected_data.pop('username')
        expected_email = expected_data.pop('email')
        expected_password = expected_data.pop('password')
        expected_creator = self.user
        serializer = self.serializer_class(context={'request': self.request})
        tested_company = serializer.create(self.create_data)
        mock_create.assert_called_with(
            expected_creator,
            expected_username,
            expected_email,
            expected_password,
            **expected_data
        )
        assert tested_company == expected_company
