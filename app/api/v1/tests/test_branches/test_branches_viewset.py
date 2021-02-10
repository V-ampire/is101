from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

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
    expected_company = CompanyProfileFactory.create()
    generate_to_db(BranchFactory, quantity=5, company=expected_company)
    generate_to_db(BranchFactory, quantity=5)
    viewset = BranchesViewSet()
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
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        mock_has_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)

    def test_list_response_for_permitted(self, mocker):
        generate_to_db(BranchFactory, quantity=10)
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
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
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
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
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.has_user_perm_to_branch')
        mock_has_branch_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_branch_perm.assert_called_with(self.tested_branch.uuid, self.admin_user.uuid)

    def test_retrieve_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_branch_perm = mocker.patch('api.v1.permissions.has_user_perm_to_branch')
        mock_has_branch_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.BranchSerializer(
            self.tested_branch, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
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
        self.create_data['company'] = self.company_user.uuid
        self.url = self.get_action_url('list')

    def test_create_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        assert mock_has_perm.call_count == 1