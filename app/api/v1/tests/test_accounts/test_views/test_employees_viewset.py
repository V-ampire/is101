from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts.factories import EmployeeUserAccountModelFactory

from company.factories import EmployeeFactory

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
    factory_class = EmployeeUserAccountModelFactory
    serializer_class = EmployeeUserAccountSerializer

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_employee = generate_to_db(EmployeeFactory)[0]
        self.tested_account = self.tested_employee.user
        self.permitted_users = self.tested_account.permitted_users
        self.permitted_clients = [self.get_api_client(user=user) for user in self.permitted_users]

    def test_list(self):
        url = self.get_action_url('list')
        generate_to_db(self.factory_class, quantity=10)
        
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        expected_data = self.serializer_class(
            get_user_model().employee_objects.all(), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve(self):
        url = self.get_action_url('detail', uuid=self.tested_account.uuid)
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        permitted_responses = [
            client.get(url) for client in self.permitted_clients
        ]
        expected_data = self.serializer_class(
            self.tested_account, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_by_admin(self):
        expected_username = fake.user_name()
        url = self.get_action_url('detail', uuid=self.tested_account.uuid)
        data = {'username': expected_username}
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        self.tested_account.refresh_from_db()
        expected_data = self.serializer_class(
            self.tested_account, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert self.tested_account.username == expected_username
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_by_permitted(self):
        expected_username = fake.user_name()
        url = self.get_action_url('detail', uuid=self.tested_account.uuid)
        data = {'username': expected_username}
        permitted_responses = [
            client.patch(url, data=data) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        expected_data = self.serializer_class(
            self.tested_account, 
        ).data

        assert self.tested_account.username == expected_username
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == expected_data

    def test_patch_password(self):
        """
        Пароль можно менять только через действие change_password.
        """
        url = self.get_action_url('detail', uuid=self.tested_account.uuid)
        expected_password = fake.password()
        data = {'password': expected_password}
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        permitted_responses = [
            client.patch(url, data=data) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        
        assert not check_password(expected_password, self.tested_account.password)
        assert admin_response.status_code == status.HTTP_400_BAD_REQUEST
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self):
        url = self.get_action_url('detail', uuid=self.tested_account.uuid)
        admin_response = self.admin_client.delete(url)
        company_response = self.company_client.delete(url)
        employee_response = self.employee_client.delete(url)
        anonymous_response = self.anonymous_client.delete(url)
        permitted_responses = [
            client.delete(url) for client in self.permitted_clients
        ]
        
        assert not get_user_model().objects.filter(uuid=self.tested_account.uuid).exists()
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_admin(self):
        data = generate_to_dict(EmployeeUserAccountModelFactory)
        expected_username = data['username']
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=data)
        employee_response = self.employee_client.post(url, data=data)
        anonymous_response = self.anonymous_client.post(url, data=data)
        
        assert get_user_model().employee_objects.filter(username=expected_username).exists()
        assert not get_user_model().employee_objects.get(username=expected_username).is_active
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_by_company(self):
        data = generate_to_dict(EmployeeUserAccountModelFactory)
        expected_username = data['username']
        url = self.get_action_url('list')
        company_response = self.company_client.post(url, data=data)
        assert get_user_model().employee_objects.filter(username=expected_username).exists()
        assert not get_user_model().employee_objects.get(username=expected_username).is_active
        assert company_response.status_code == status.HTTP_201_CREATED

    def test_activate_by_admin(self):
        url = self.get_action_url('activate', uuid=self.tested_account.uuid)
        self.tested_account.deactivate()
        admin_response = self.admin_client.patch(url)
        company_response = self.company_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        self.tested_account.refresh_from_db()
        
        assert self.tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_activate_by_permitted(self):
        url = self.get_action_url('activate', uuid=self.tested_account.uuid)
        self.tested_account.deactivate()
        permitted_responses = [
            client.patch(url) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        
        assert self.tested_account.is_active
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

    def test_deactivate_by_admin(self):
        url = self.get_action_url('deactivate', uuid=self.tested_account.uuid)
        admin_response = self.admin_client.patch(url)
        company_response = self.company_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        self.tested_account.refresh_from_db()
        
        assert not self.tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deactivate_by_permitted(self):
        url = self.get_action_url('deactivate', uuid=self.tested_account.uuid)
        permitted_responses = [
            client.patch(url) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        
        assert not self.tested_account.is_active
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

    def test_activate_by_permitted(self):
        url = self.get_action_url('activate', uuid=self.tested_account.uuid)
        self.tested_account.deactivate()
        permitted_responses = [
            client.patch(url) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        
        assert self.tested_account.is_active
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

    def test_change_password_by_admin(self):
        url = self.get_action_url('change-password', uuid=self.tested_account.uuid)
        expected_password = fake.password()
        data = {
            'password1': expected_password,
            'password2': expected_password
        }
        admin_response = self.admin_client.patch(url, data=data)
        company_response = self.company_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        self.tested_account.refresh_from_db()
        
        assert check_password(expected_password, self.tested_account.password)
        assert admin_response.status_code == status.HTTP_200_OK
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_by_permitted(self):
        url = self.get_action_url('change-password', uuid=self.tested_account.uuid)
        expected_password = fake.password()
        data = {
            'password1': expected_password,
            'password2': expected_password
        }
        permitted_responses = [
            client.patch(url, data=data) for client in self.permitted_clients
        ]
        self.tested_account.refresh_from_db()
        
        assert check_password(expected_password, self.tested_account.password)
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

