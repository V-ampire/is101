from rest_framework import status
from rest_framework.test import APIRequestFactory

from accounts.factories import CompanyUserAccountModelFactory

from companies.factories import BranchFactory, CompanyProfileFactory
from companies.models import Branch

from api.v1.tests.base import BaseViewSetTest

from api.v1.branches import serializers
from api.v1.branches.views import BranchesViewSet

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
def test_get_queryset():
    rf =  APIRequestFactory()
    expected_company = CompanyProfileFactory.create()
    generate_to_db(BranchFactory, quantity=5, company=expected_company)
    generate_to_db(BranchFactory, quantity=5)
    request = rf.get('/branches/')
    request.query_params = {}
    viewset = BranchesViewSet()
    viewset.request = request
    viewset.kwargs = {'company_uuid': expected_company.uuid}
    expected = list(Branch.objects.filter(company__uuid=expected_company.uuid))
    tested = list(viewset.get_queryset())
    assert tested == expected


@pytest.mark.django_db
class TestListAction(BaseViewSetTest):
    app_name = 'api_v1'
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.url = self.get_action_url('list', company_uuid=self.tested_company.uuid)

    def test_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.branches.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        mock_has_perm.assert_called_once()

    def test_list_response_for_permitted(self, mocker):
        generate_to_db(BranchFactory, quantity=10)
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.BranchListSerializer(
            Branch.objects.filter(company__uuid=self.tested_company.uuid), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_list_response_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
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
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.tested_branch = BranchFactory.create(company=self.tested_company)
        self.url = self.get_action_url(
            'detail', company_uuid=self.tested_company.uuid, uuid=self.tested_branch.uuid
        )

    def test_retrieve_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        mock_has_company_perm.assert_called_once()
        mock_has_branch_perm.assert_called_once()

    def test_retrieve_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.BranchSerializer(
            self.tested_branch, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
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
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.create_data = generate_to_dict(BranchFactory)
        self.create_data.pop('company')
        self.url = self.get_action_url('list', company_uuid=self.tested_company.uuid)

    def test_create_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        mock_has_company_perm.assert_called_once()

    def test_create_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        expected_branch = Branch.objects.get(**self.create_data)
        expected_data = serializers.BranchSerializer(
            expected_branch, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data

    def test_create_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
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
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.tested_branch = BranchFactory.create(company=self.tested_company)
        self.patch_data = {
            'phone': fake.phone_number()
        }
        self.url = self.get_action_url(
            'detail', company_uuid=self.tested_company.uuid, uuid=self.tested_branch.uuid
        )

    def test_patch_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        mock_has_company_perm.assert_called_once()
        mock_has_branch_perm.assert_called_once()

    def test_patch_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        self.tested_branch.refresh_from_db()
        expected_data = serializers.BranchSerializer(
            self.tested_branch, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert self.tested_branch.phone == self.patch_data['phone']
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_patch_for_forbidden_to_company(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_patch_for_forbidden_to_branch(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_pacth_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data=self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestDestroyAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.tested_branch = BranchFactory.create(company=self.tested_company)
        self.url = self.get_action_url(
            'detail', company_uuid=self.tested_company.uuid, uuid=self.tested_branch.uuid
        )

    def test_destroy_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.branches.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        mock_has_perm.call_count == 1

    def test_destroy_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.branches.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = True
        mock_delete = mocker.patch('api.v1.branches.views.utils.delete_branch')
        admin_response = self.admin_client.delete(self.url)

        mock_delete.assert_called_with(self.tested_branch.uuid)
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT

    def test_patch_for_forbidden_to_branch(self, mocker):
        mock_has_perm = mocker.patch('api.v1.branches.views.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_pacth_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.delete(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestToArchiveAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.tested_branch = BranchFactory.create(company=self.tested_company)
        self.url = self.get_action_url(
            'to-archive', company_uuid=self.tested_company.uuid, uuid=self.tested_branch.uuid
        )
        self.expected_data = {'status': 'Филиал переведен в архив.'}

    def test_to_archive_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        mock_has_company_perm.assert_called_once()
        mock_has_branch_perm.assert_called_once()

    def test_to_archive_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.branches.views.utils.branch_to_archive')
        expected_force = False
        admin_response = self.admin_client.patch(self.url)
        mock_to_archive.assert_called_with(self.tested_branch.uuid, force=expected_force)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_force_to_archive_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.branches.views.utils.branch_to_archive')
        expected_force = True
        data = {'force': expected_force}
        admin_response = self.admin_client.patch(self.url, data=data, format='json')
        mock_to_archive.assert_called_with(self.tested_branch.uuid, force=expected_force)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_force_to_archive_invalid_content_type(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.branches.views.utils.branch_to_archive')
        expected_force = True
        data = {'force': expected_force}
        expected_data = {'detail': 'Данные должны быть переданы в формате application/json.'}
        admin_response = self.admin_client.patch(self.url, data=data)
        assert mock_to_archive.call_count == 0
        assert admin_response.status_code == status.HTTP_400_BAD_REQUEST
        assert admin_response.json() == expected_data

    def test_patch_for_forbidden_to_branch(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_pacth_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestToWorkAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branches'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = CompanyProfileFactory.create()
        self.tested_branch = BranchFactory.create(company=self.tested_company)
        self.url = self.get_action_url(
            'to-work', company_uuid=self.tested_company.uuid, uuid=self.tested_branch.uuid
        )
        self.expected_data = {'status': 'Филиал в рабочем статусе.'}

    def test_to_work_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        mock_has_company_perm.assert_called_once()
        mock_has_branch_perm.assert_called_once()

    def test_to_work_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_object_permission')
        mock_has_branch_perm.return_value = True
        mock_to_work = mocker.patch('api.v1.branches.views.utils.branch_to_work')
        admin_response = self.admin_client.patch(self.url)
        mock_to_work.assert_called_with(self.tested_branch.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_work_for_forbidden_to_branch(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.IsCompanyOwnerOrAdmin.has_permission')
        mock_has_company_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_to_work_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data