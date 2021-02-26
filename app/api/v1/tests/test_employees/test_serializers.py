from rest_framework.serializers import ValidationError

from api.v1.branches import serializers

from companies.factories import CompanyProfileFactory, BranchFactory, EmployeeProfileFactory

from factory_generator import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCreateEmployeeSerializer():

    def setup_method(self, method):
        self.create_data = generate_to_dict(EmployeeProfileFactory)

    def test_validate_calls_validate_user(self, mocker):
        mock_is_valid_user = mocker.patch('api.v1.employees.serializers.EmployeeUserAccountSerializer.is_valid')
