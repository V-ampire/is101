from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts.factories import EmployeeUserAccountModelFactory

from api.v1.tests.base import BaseViewSetTest

from api.v1.accounts.serializers import EmployeeUserAccountSerializer

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestListAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.url = self.get_action_url('list')

    def test_permisson(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_list_response_for_permitted(self, mocker):
        generate_to_db(EmployeeUserAccountModelFactory, quantity=10)
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = EmployeeUserAccountSerializer(
            get_user_model().employee_objects.all(), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_list_response_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_list_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.get(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data

    
@pytest.mark.django_db
class TestRetrieveAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_account = EmployeeUserAccountModelFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_account.uuid)

    def test_permisson(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_retrieve_response_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.get(self.url)
        expected_data = EmployeeUserAccountSerializer(
            self.tested_account, 
            context={'request': company_response.wsgi_request}
        ).data
        assert company_response.status_code == status.HTTP_200_OK
        assert company_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_retrieve_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.get(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestPatchAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.patch_data = {
            'email': fake.company_email()
        }
        self.tested_account = EmployeeUserAccountModelFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_account.uuid)

    def test_patch_permisiion(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert mock_has_perm.call_count == 1

    def test_patch_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.patch(self.url, data=self.patch_data)
        self.tested_account.refresh_from_db()
        expected_data = EmployeeUserAccountSerializer(
            self.tested_account, 
            context={'request': company_response.wsgi_request}
        ).data
        assert company_response.status_code == status.HTTP_200_OK
        assert company_response.json() == expected_data
        assert self.tested_account.email == self.patch_data['email']

    def test_patch_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_patch_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data=self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestDeativateAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_account = EmployeeUserAccountModelFactory.create()
        self.url = self.get_action_url('deactivate', uuid=self.tested_account.uuid)
        self.expected_data = {'status': 'Пользователь в неактивном статусе.'}

    def test_deactivate_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_deactivate_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        self.tested_account.refresh_from_db()
        assert not self.tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_deactivate_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_deactivate_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestAtivateAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_account = EmployeeUserAccountModelFactory.create(is_active=False)
        self.url = self.get_action_url('activate', uuid=self.tested_account.uuid)
        self.expected_data = {'status': 'Пользователь в активном статусе.'}

    def test_activate_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_activate_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        self.tested_account.refresh_from_db()
        assert self.tested_account.is_active
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_deactivate_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_deactivate_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestChangePasswordAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_account = EmployeeUserAccountModelFactory.create(is_active=False)
        self.url = self.get_action_url('change-password', uuid=self.tested_account.uuid)
        self.expected_password = fake.password()
        self.patch_data = {
            'password1': self.expected_password,
            'password2': self.expected_password,
        }
        self.expected_data = {'status': 'Пароль изменен.'}

    def test_change_password_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data= self.patch_data)
        mock_has_perm.call_count == 1

    def test_change_password_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = True
        mock_change = mocker.patch('api.v1.accounts.mixins.change_password')
        admin_response = self.admin_client.patch(self.url, data= self.patch_data)
        
        mock_change.assert_called_with(self.tested_account.pk, self.expected_password)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_change_password_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.accounts.views.IsPermittedToEmployeeUser.has_object_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data= self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_change_password_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data= self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
