from rest_framework.serializers import ValidationError

from api.v1.companies import serializers

from company.factories import CompanyFactory
from company.models import Company

from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCompanyCreateSerializer():

    def test_validate_user_create(self, mocker, company_user):
        mock_validate_user = mocker.patch('api.v1.companies.serializers.validate_user_for_create')
        mock_validate_user.return_value = company_user
        serializer = serializers.CompanyCreateSerializer()
        expected_uuid = company_user.uuid
        tested_user = serializer.validate_user(expected_uuid)
        assert tested_user == company_user
        assert mock_validate_user.call_count == 1
        mock_validate_user.assert_called_with(uuid=expected_uuid)
    
    def test_create_company(self, company_user, factory_as_dict):
        company_data = factory_as_dict(CompanyFactory)
        company_data.pop('user')
        create_data = company_data.copy()
        create_data['user'] = company_user
        serializer = serializers.CompanyCreateSerializer()
        expected_company = serializer.create(create_data)
        assert Company.objects.filter(user=company_user, title=company_data['title']).exists()
        assert expected_company == Company.objects.get(title=company_data['title'])