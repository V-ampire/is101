from rest_framework.serializers import ValidationError

from api.v1.branches import serializers

from companies.factories import CompanyProfileFactory, BranchFactory

from factory_generator import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCreateBranchSerializer():

    def test_validate_company_with_company_does_not_exist(self):
        serializer = serializers.BranchCreateSerializer()
        company_uuid = fake.uuid4()
        exp_message = f'Юрлицо с uuid={company_uuid} не существует.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            serializer.validate_company(company_uuid)
        assert exc_info.value.args[0] == exp_message
    
    def test_success_validate(self):
        expected_company = CompanyProfileFactory.create()
        serializer = serializers.BranchCreateSerializer()
        tested_uuid = serializer.validate_company(expected_company.uuid)
        assert tested_uuid == expected_company.uuid

    def test_create(self, mocker):
        mock_create = mocker.patch('api.v1.branches.serializers.create_branch')
        expected_company_uuid = fake.uuid4()
        create_data = generate_to_dict(BranchFactory)
        create_data.pop('company')
        expected_branch_data = create_data.copy()
        create_data['company'] = expected_company_uuid
        serializer = serializers.BranchCreateSerializer()
        serializer.create(create_data)
        mock_create.assert_called_with(expected_company_uuid, **expected_branch_data)

