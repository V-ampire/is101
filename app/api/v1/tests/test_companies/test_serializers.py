from rest_framework.serializers import ValidationError as APIValidationError

from api.v1.companies import serializers

from accounts.factories import CompanyUserAccountModelFactory, AdminUserAccountModelFactory

from companies.factories import CompanyProfileFactory
from companies.models import CompanyProfile

from factory_generator import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCompanyCreateSerializer():

    def setup_method(self, method):
        self.user = CompanyUserAccountModelFactory.create()
        self.create_data = generate_to_dict(CompanyProfileFactory)
        self.create_data.pop('user')
        self.serializer_class = serializers.CompanyCreateSerializer

    def test_validate_user(self, mocker):
        mock_validate_user = mocker.patch(
            'api.v1.companies.serializers.validators.validate_company_user'
        )
        serializer = self.serializer_class()
        serializer.validate_user(self.user.uuid)
        mock_validate_user.assert_called_with(self.user)

    def test_validate_user_with_user_not_exist(self):
        user_uuid = fake.uuid4()
        serializer = self.serializer_class()
        with pytest.raises(APIValidationError):
            serializer.validate_user(user_uuid)
    
    def test_create_company(self, mocker):
        mock_create = mocker.patch('api.v1.companies.serializers.utils.create_company')
        expected_company = mocker.Mock()
        mock_create.return_value = expected_company
        expected_data = self.create_data.copy()
        self.create_data['user'] = self.user.uuid
        serializer = self.serializer_class()
        tested_company = serializer.create(self.create_data)

        mock_create.assert_called_with(user_uuid=self.user.uuid, **expected_data)
        assert tested_company == expected_company
