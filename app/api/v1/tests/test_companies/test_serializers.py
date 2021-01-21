from rest_framework.serializers import ValidationError

from api.v1.companies import serializers

from accounts.factories import CompanyUserAccountModelFactory

from company.factories import CompanyFactory
from company.models import Company

from factory_generator import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCompanyCreateSerializer():

    def setup_method(self, method):
        self.user = CompanyUserAccountModelFactory.create()
        self.create_data = generate_to_dict(CompanyFactory)
        self.create_data.pop('user')
        self.serializer_class = serializers.CompanyCreateSerializer

    def test_validate_user(self, mocker):
        mock_validate_user = mocker.patch(
            'api.v1.companies.serializers.validators.validate_user_data_for_create'
        )
        mock_validate_user.return_value = self.user
        serializer = self.serializer_class()
        expected_uuid = self.user.uuid
        tested_user_uuid = serializer.validate_user(expected_uuid)

        assert tested_user_uuid == expected_uuid
        mock_validate_user.assert_called_with(uuid=expected_uuid)
    
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
