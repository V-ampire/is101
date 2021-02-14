from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts.factories import EmployeeUserAccountModelFactory

from companies.factories import EmployeeProfileFactory

from api.v1.tests.base import BaseViewSetTest

from api.v1.accounts.serializers import EmployeeUserAccountSerializer

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestViewSet(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_user = EmployeeUserAccountModelFactory.create()

    def test_list(self, mocker):
        url = self.get_action_url('list')
        EmployeeUserAccountModelFactory.create_batch(10)
        
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)

        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve(self):
        url = self.get_action_url('detail', uuid=self.tested_user.uuid)
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)

        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

