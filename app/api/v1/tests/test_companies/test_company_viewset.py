from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory

from company.factories import CompanyFactory
from company.models import Company

from api.v1.tests.base import BaseViewSetTest

from api.v1.companies import serializers

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestViewset(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'
    factory_class = CompanyFactory

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = generate_to_db(CompanyFactory)[0]
        self.permitted_users = self.tested_company.permitted_users
        self.permitted_clients = [self.get_api_client(user=user) for user in self.permitted_users]

    def test_list(self):
        url = self.get_action_url('list')
        generate_to_db(self.factory_class, quantity=10)
        
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        permitted_responses = [
            client.get(url) for client in self.permitted_clients
        ]
        expected_data = serializers.CompanyListSerializer(
            Company.objects.all().order_by('-status'), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_for_admins(self):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)       
        admin_response = self.admin_client.get(url)
        company_response = self.company_client.get(url)
        employee_response = self.employee_client.get(url)
        anonymous_response = self.anonymous_client.get(url)
        expected_data = serializers.CompanySerializerForAdmin(
            self.tested_company, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert company_response.status_code == status.HTTP_403_FORBIDDEN
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_for_permitted(self):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        permitted_responses = [
            client.get(url) for client in self.permitted_clients
        ]
        expected_data = [
            serializers.CompanySerializerForPermitted(
            self.tested_company, 
            context={'request': response.wsgi_request}
        ).data for response in permitted_responses
        ]
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK
            expected_data = serializers.CompanySerializerForPermitted(
                self.tested_company, 
                context={'request': response.wsgi_request}
            ).data
            assert expected_data == response.json()

    def test_create(self):
        data = generate_to_dict(CompanyFactory)
        data['user'] = self.company_user.uuid
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=data)
        employee_response = self.employee_client.post(url, data=data)
        anonymous_response = self.anonymous_client.post(url, data=data)
        tested_company = Company.objects.get(title=data['title'])
        
        assert tested_company.user == self.company_user
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_with_invalid_user(self):
        data = generate_to_dict(CompanyFactory)
        data['user'] = self.employee_user.uuid
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=data)
        employee_response = self.employee_client.post(url, data=data)
        anonymous_response = self.anonymous_client.post(url, data=data)
        
        assert not Company.objects.filter(title=data['title']).exists()
        assert admin_response.status_code == status.HTTP_400_BAD_REQUEST
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_by_admin(self):
        data = generate_to_dict(CompanyFactory)
        data.pop('user')
        data.pop('logo')
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.patch(url, data=data)
        employee_response = self.employee_client.patch(url, data=data)
        anonymous_response = self.anonymous_client.patch(url, data=data)
        expected_data = serializers.CompanySerializerForAdmin(
            self.tested_company, 
            context={'request': admin_response.wsgi_request}
        ).data

        assert Company.objects.filter(**data).exists()
        assert admin_response.status_code == status.HTTP_200_OK
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_by_permitted(self):
        data = generate_to_dict(CompanyFactory)
        data.pop('user')
        data.pop('logo')
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        permitted_responses = [
            client.patch(url, data=data) for client in self.permitted_clients
        ]
        assert Company.objects.filter(**data).exists()
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

    def test_disable_patch_user_by_admin(self):
        new_user = CompanyUserAccountModelFactory.create()
        data = {
            'user': new_user.uuid
        }
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.patch(url, data=data)
        self.tested_company.refresh_from_db()

        assert not self.tested_company.user.uuid == new_user.uuid
        assert admin_response.status_code == status.HTTP_200_OK

    def test_disable_patch_user_by_permitted(self):
        new_user = CompanyUserAccountModelFactory.create()
        data = {
            'user': new_user.uuid
        }
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        permitted_responses = [
            client.patch(url, data=data) for client in self.permitted_clients
        ]
        self.tested_company.refresh_from_db()

        assert not self.tested_company.user.uuid == new_user.uuid
        for response in permitted_responses:
            assert response.status_code == status.HTTP_200_OK

    def test_delete(self, mocker):
        mock_delete = mocker.patch('api.v1.companies.views.utils.delete_company')
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.delete(url)
        employee_response = self.employee_client.delete(url)
        anonymous_response = self.anonymous_client.delete(url)
        permitted_responses = [
            client.delete(url) for client in self.permitted_clients
        ]

        mock_delete.assert_called_with(self.tested_company.uuid)
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_activate(self, mocker):
        mock_action = mocker.patch('api.v1.companies.views.utils.activate_company')
        url = self.get_action_url('activate', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        permitted_responses = [
            client.patch(url) for client in self.permitted_clients
        ]

        mock_action.assert_called_with(self.tested_company.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_archivate(self, mocker):
        mock_action = mocker.patch('api.v1.companies.views.utils.archivate_company')
        url = self.get_action_url('archivate', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.patch(url)
        employee_response = self.employee_client.patch(url)
        anonymous_response = self.anonymous_client.patch(url)
        permitted_responses = [
            client.patch(url) for client in self.permitted_clients
        ]

        mock_action.assert_called_with(self.tested_company.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert employee_response.status_code == status.HTTP_403_FORBIDDEN
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        for response in permitted_responses:
            assert response.status_code == status.HTTP_403_FORBIDDEN
