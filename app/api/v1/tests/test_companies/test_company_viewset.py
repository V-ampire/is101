from django.contrib.auth import get_user_model

from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory
from accounts.emails import MessageField

from companies.factories import CompanyProfileFactory
from companies.models import CompanyProfile

from api.v1.tests.base import BaseViewSetTest

from api.v1.companies import serializers

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()

@pytest.mark.django_db
class TestListAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.url = self.get_action_url('list')

    def test_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_list_response_for_permitted(self, mocker):
        generate_to_db(CompanyProfileFactory, quantity=10)
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.CompanyListSerializer(
            CompanyProfile.objects.all().order_by('-status'), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_list_response_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
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
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_company.uuid)

    def test_retrieve_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        mock_has_perm.assert_called_once()

    def test_retrieve_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.get(self.url)
        expected_data = serializers.CompanyDetailSerializer(
            self.tested_company, 
            context={'request': company_response.wsgi_request}
        ).data
        assert company_response.status_code == status.HTTP_200_OK
        assert company_response.json() == expected_data

    def test_retrieve_for_admin(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.CompanyDetailSerializer(
            self.tested_company, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_retrive_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.get(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestCreateAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.create_data = generate_to_dict(CompanyProfileFactory)
        self.create_data.pop('user')
        self.create_data['username'] = f'{fake.user_name()}@{fake.user_name()}'
        self.create_data['password'] = fake.password()
        self.create_data['email'] = fake.email()
        self.url = self.get_action_url('list')

    def test_create_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        assert mock_has_perm.call_count == 1

    def test_create_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_send_task = mocker.patch('api.v1.companies.views.send_account_created_message.delay')
        mock_get_fields = mocker.patch('api.v1.companies.views.get_email_fields')
        expected_email_fields = fake.pylist()
        mock_get_fields.return_value = expected_email_fields
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        import pdb; pdb.set_trace()
        expected_company = CompanyProfile.objects.get(title=self.create_data['title'])
        expected_data = serializers.CompanyDetailSerializer(
            expected_company, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data
        mock_send_task.assert_called_with(self.admin_user.uuid, expected_email_fields)

    def test_create_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_create_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.post(self.url, data=self.create_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestPatchAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.patch_data = {
            'title': fake.company()
        }
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_company.uuid)

    def test_patch_permisiion(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert mock_has_perm.call_count == 2

    def test_patch_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.patch(self.url, data=self.patch_data)
        self.tested_company.refresh_from_db()
        expected_data = serializers.CompanyDetailSerializer(
            self.tested_company, 
            context={'request': company_response.wsgi_request}
        ).data
        assert company_response.status_code == status.HTTP_200_OK
        assert company_response.json() == expected_data
        assert self.tested_company.title == self.patch_data['title']
    
    def test_patch_for_admin(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        self.tested_company.refresh_from_db()
        expected_data = serializers.CompanyDetailSerializer(
            self.tested_company, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert self.tested_company.title == self.patch_data['title']

    def test_patch_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_patch_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data=self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestDestroyAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_company.uuid)

    def test_destroy_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        mock_has_perm.call_count == 1

    def test_destroy_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_delete = mocker.patch('api.v1.companies.views.utils.delete_company')
        admin_response = self.admin_client.delete(self.url)

        mock_delete.assert_called_with(self.tested_company.uuid)
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT

    def test_destroy_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        mock_delete = mocker.patch('api.v1.companies.views.utils.delete_company')
        admin_response = self.admin_client.delete(self.url)
        assert mock_delete.call_count == 0
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN

    def test_destroy_for_anonymous_user(self, mocker):
        mock_delete = mocker.patch('api.v1.companies.views.utils.delete_company')
        anonymous_response = self.anonymous_client.delete(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
        assert mock_delete.call_count == 0


@pytest.mark.django_db
class TestToArchiveAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('to-archive', uuid=self.tested_company.uuid)
        self.expected_data = {'status': 'Юрлицо переведено в архив. Учетная запись отключена.'}

    def test_to_archive_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_to_archive_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.companies.views.utils.company_to_archive')
        expected_force = False
        admin_response = self.admin_client.patch(self.url)
        mock_to_archive.assert_called_with(self.tested_company.uuid, force=expected_force)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_force_to_archive_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.companies.views.utils.company_to_archive')
        expected_force = True
        data = {'force': expected_force}
        admin_response = self.admin_client.patch(self.url, data=data, format='json')
        mock_to_archive.assert_called_with(self.tested_company.uuid, force=expected_force)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_force_to_archive_invalid_content_type(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.companies.views.utils.company_to_archive')
        expected_force = True
        data = {'force': expected_force}
        expected_data = {'detail': 'Данные должны быть переданы в формате application/json.'}
        admin_response = self.admin_client.patch(self.url, data=data)
        assert mock_to_archive.call_count == 0
        assert admin_response.status_code == status.HTTP_400_BAD_REQUEST
        assert admin_response.json() == expected_data

    def test_to_archive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        mock_to_archive = mocker.patch('api.v1.companies.views.utils.company_to_archive')
        admin_response = self.admin_client.patch(self.url)
        assert mock_to_archive.call_count == 0
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_to_archive_for_anonymous_user(self, mocker):
        mock_to_archive = mocker.patch('api.v1.companies.views.utils.company_to_archive')
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
        assert mock_to_archive.call_count == 0


@pytest.mark.django_db
class TestToWorkAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'companies'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('to-work', uuid=self.tested_company.uuid)
        self.expected_data = {'status': 'Юрлицо в рабочем статусе. Учетная запись активирована.'}

    def test_to_work_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_to_work_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_work = mocker.patch('api.v1.companies.views.utils.company_to_work')
        admin_response = self.admin_client.patch(self.url)
        mock_to_work.assert_called_with(self.tested_company.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_work_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        mock_to_work = mocker.patch('api.v1.companies.views.utils.company_to_work')
        admin_response = self.admin_client.patch(self.url)
        assert mock_to_work.call_count == 0
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_to_work_for_anonymous_user(self, mocker):
        mock_to_work = mocker.patch('api.v1.companies.views.utils.company_to_work')
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
        assert mock_to_work.call_count == 0