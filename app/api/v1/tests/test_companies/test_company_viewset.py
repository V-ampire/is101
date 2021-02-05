from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory

from companies.factories import CompanyFactory
from companies.models import CompanyProfile

from api.v1.tests.base import BaseViewSetTest

from api.v1.companies import serializers

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestViewset(BaseViewSetTest):
    # Тест проверки доступа к каждому действию
    # Тест успешного ответа
    # Тест отказаного ответа
    # Тест ответа на анонимный запрос

    app_name = 'api_v1'
    url_basename = 'companies'
    factory_class = CompanyFactory

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = generate_to_db(CompanyFactory)[0]
    
    def test_list_permission(self, mocker):
        url = self.get_action_url('list')
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(url)
        assert mock_has_perm.call_count == 1
    
    def test_list_response_for_permitted(self, mocker):
        generate_to_db(self.factory_class, quantity=10)
        url = self.get_action_url('list')
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(url)
        expected_data = serializers.CompanyListSerializer(
            Company.objects.all().order_by('-status'), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_list_response_for_forbidden(self, mocker)
        url = self.get_action_url('list')
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.get(url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_permission(self, mocker):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(url)
        mock_has_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)

    def test_retrieve_for_permitted(self, mocker):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(url)
        expected_data = serializers.CompanyListSerializer(
            self.tested_company, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_for_anonymous_user(self):
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        anonymous_response = self.anonymous_client.get(url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        data = generate_to_dict(CompanyFactory)
        data['user'] = self.company_user.uuid
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=data)
        assert mock_has_perm.call_count == 1

    def test_create_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        create_data = generate_to_dict(CompanyFactory)
        create_data['user'] = self.company_user.uuid
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=create_data)
        self.company_user.refresh_from_db()
        expected_company = self.comany.user.company_profile
        expected_data = serializers.CompanyListSerializer(
            expected_company, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data

    def test_create_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        create_data = generate_to_dict(CompanyFactory)
        create_data['user'] = self.company_user.uuid
        url = self.get_action_url('list')
        admin_response = self.admin_client.post(url, data=create_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_for_anonymous_user(self):
        create_data = generate_to_dict(CompanyFactory)
        create_data['user'] = self.company_user.uuid
        url = self.get_action_url('list')
        anonymous_response = self.anonymous_client.post(url, data=create_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = True
        data = generate_to_dict(CompanyFactory)
        data.pop('user')
        data.pop('logo')
        url = self.get_action_url('detail', uuid=self.tested_company.uuid)
        admin_response = self.admin_client.get(url)
        mock_has_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)





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
