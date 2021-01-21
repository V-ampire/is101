from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory

from api.v1.tests.base import BaseViewSetTest

from api.v1.accounts.serializers import CompanyUserAccountSerializer

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestViewSet(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'account-companies'

    def test_list(self):
        url = self.get_action_url('list')
        generate_to_db(CompanyUserAccountModelFactory, quantity=10)
        
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        expected_data = CompanyUserAccountSerializer(
            get_user_model().company_objects.all(), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        url = self.get_action_url('detail', uuid=tested_account.uuid)
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        expected_data = CompanyUserAccountSerializer(
            tested_account, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        expected_username = fake.user_name()
        url = self.get_action_url('detail', uuid=tested_account.uuid)
        data = {'username': expected_username}
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        tested_account.refresh_from_db()
        expected_data = CompanyUserAccountSerializer(
            tested_account, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert tested_account.username == expected_username
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_password(self):
        """
        Пароль можно менять только через действие change_password.
        """
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        url = self.get_action_url('detail', uuid=tested_account.uuid)
        expected_password = fake.password()
        data = {'password': expected_password}
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        tested_account.refresh_from_db()
        
        assert not check_password(expected_password, tested_account.password)
        assert admin_response.status_code == status.HTTP_400_BAD_REQUEST
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        url = self.get_action_url('detail', uuid=tested_account.uuid)
        admin_response = self.admin_client.delete(url)
        company_response = self.company_client.delete(url)
        employee_response = self.employee_client.delete(url)
        anonymous_response = self.anonymous_client.delete(url)
        
        assert not get_user_model().objects.filter(uuid=tested_account.uuid).exists()
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create(self):
        data = generate_to_dict(CompanyUserAccountModelFactory)
        expected_username = data['username']
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=data)
        company_response = self.company_client.post(url, data=data)
        employee_response = self.employee_client.post(url, data=data)
        anonymous_response = self.anonymous_client.post(url, data=data)
        
        assert get_user_model().company_objects.filter(username=expected_username).exists()
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_activate(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory, is_active=False)[0]
        url = self.get_action_url('activate', uuid=tested_account.uuid)
        admin_response = self.admin_client.patch(url)
        company_response = self.company_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        tested_account.refresh_from_db()
        
        assert tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deativate(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        url = self.get_action_url('deactivate', uuid=tested_account.uuid)
        admin_response = self.admin_client.patch(url)
        company_response = self.company_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        tested_account.refresh_from_db()
        
        assert not tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password(self):
        tested_account = generate_to_db(CompanyUserAccountModelFactory)[0]
        url = self.get_action_url('change-password', uuid=tested_account.uuid)
        expected_password = fake.password()
        data = {
            'password1': expected_password,
            'password2': expected_password
        }
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        tested_account.refresh_from_db()
        
        assert check_password(expected_password, tested_account.password)
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
