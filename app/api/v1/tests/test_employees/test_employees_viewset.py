from rest_framework import status

from api.v1.employees import serializers
from api.v1.employees.views import EmployeeViewSet

from api.v1.tests.base import BaseViewSetTest

from companies import factories
from companies.models import EmployeeProfile

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
def test_get_queryset():
    expected_branch = factories.BranchFactory.create()
    generate_to_db(factories.EmployeeProfileFactory, quantity=5, branch=expected_branch)
    generate_to_db(factories.EmployeeProfileFactory, quantity=5)
    viewset = EmployeeViewSet()
    viewset.kwargs = {'branch_uuid': expected_branch.uuid}
    expected = list(EmployeeProfile.objects.filter(branch__uuid=expected_branch.uuid))
    tested = list(viewset.get_queryset())
    assert tested == expected


@pytest.mark.django_db
class TestListAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.url = self.get_action_url(
            'list', company_uuid=self.tested_company.uuid, branch_uuid=self.tested_branch.uuid
        )

    def test_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        mock_has_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)

    def test_list_response_for_permitted(self, mocker):
        generate_to_db(factories.EmployeeProfileFactory, quantity=10, branch=self.tested_branch)
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.EmployeeListSerizlizer(
            EmployeeProfile.objects.filter(branch__uuid=self.tested_branch.uuid), 
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
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'detail', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )

    def test_retrieve_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.get(self.url)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_retrieve_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = serializers.EmployeeSerializer(
            self.tested_employee, 
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
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.create_data = generate_to_dict(factories.EmployeeProfileFactory)
        self.create_data.pop('user')
        self.create_data.pop('employee_position')
        self.create_data.pop('branch')
        self.create_data['username'] = f'{fake.user_name()}@{fake.user_name()}'
        self.create_data['password'] = fake.password()
        self.create_data['email'] = fake.email()
        self.url = self.get_action_url(
            'list', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
        )
    
    def test_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        mock_has_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)

    def test_create_without_position_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        expected_employee = EmployeeProfile.objects.get(pasport=self.create_data['pasport'])
        expected_data = serializers.EmployeeSerializer(
            expected_employee, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data
        assert expected_employee.position == EmployeeProfile.DEFAULT_POSTITION

    def test_create_with_position_for_permitted(self, mocker):
        expected_position = factories.PositionFactory.create()
        self.create_data['position'] = expected_position.uuid
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        expected_employee = EmployeeProfile.objects.get(pasport=self.create_data['pasport'])
        expected_data = serializers.EmployeeSerializer(
            expected_employee, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data
        assert expected_employee.position == expected_position

    def test_create_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
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
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'detail', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
        self.patch_data = {
            'fio': fake.name()
        }

    def test_patch_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_patch_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        self.tested_employee.refresh_from_db()
        expected_data = serializers.EmployeeSerializer(
            self.tested_employee, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert self.tested_employee.fio == self.patch_data['fio']
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_patch_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
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
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'detail', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
    
    def test_destroy_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_destroy_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        mock_delete = mocker.patch('api.v1.employees.views.utils.delete_employee')
        admin_response = self.admin_client.delete(self.url)

        mock_delete.assert_called_with(self.tested_employee.uuid)
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT

    def test_destroy_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_destroy_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.delete(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestToArchiveAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'to-archive', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
        self.expected_data = {'status': 'Работник переведен в архив. Учетная запись отключена.'}

    def test_to_archive_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_to_archive_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.employees.views.utils.employee_to_archive')
        admin_response = self.admin_client.patch(self.url)
        mock_to_archive.assert_called_with(self.tested_employee.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_archive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_to_archive_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestToWorkAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'to-work', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
        self.expected_data = {'status': 'Работник в рабочем статусе. Учетная запись активирована.'}

    def test_to_work_permission(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_to_work_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        mock_to_work = mocker.patch('api.v1.employees.views.utils.employee_to_work')
        admin_response = self.admin_client.patch(self.url)
        mock_to_work.assert_called_with(self.tested_employee.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_work_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_to_work_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestChangePositionAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'change-position', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
        self.expected_position = factories.PositionFactory.create()
        self.patch_data = {'position': self.expected_position.uuid}

    def test_change_position_permissions(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_change_position_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        mock_change = mocker.patch('api.v1.employees.views.utils.change_employee_position')
        mock_change.return_value = self.tested_employee
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        expected_data = serializers.EmployeeSerializer(
            self.tested_employee, 
            context={'request': admin_response.wsgi_request}
        ).data
        mock_change.assert_called_with(self.tested_employee.uuid, self.expected_position.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_change_position_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_change_position_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data=self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestChangeBranchAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'company-branch-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_company = factories.CompanyProfileFactory.create()
        self.tested_branch = factories.BranchFactory.create(company=self.tested_company)
        self.tested_employee = factories.EmployeeProfileFactory.create(branch=self.tested_branch)
        self.url = self.get_action_url(
            'change-branch', 
            company_uuid=self.tested_company.uuid, 
            branch_uuid=self.tested_branch.uuid,
            uuid=self.tested_employee.uuid
        )
        self.expected_branch = factories.BranchFactory.create(company=self.tested_company)
        self.patch_data = {'branch': self.expected_branch.uuid}
    
    def test_change_branch_permissions(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        mock_has_company_perm.assert_called_with(self.tested_company.uuid, self.admin_user.uuid)
        mock_has_employee_perm.assert_called_with(self.tested_employee.uuid, self.admin_user.uuid)

    def test_change_branch_for_permitted(self, mocker):
        mock_has_company_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_company_perm.return_value = True
        mock_has_employee_perm = mocker.patch('api.v1.permissions.has_user_perm_to_employee')
        mock_has_employee_perm.return_value = True
        mock_change = mocker.patch('api.v1.employees.views.utils.transfer_employee_to_branch')
        mock_change.return_value = self.tested_employee
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        expected_data = serializers.EmployeeSerializer(
            self.tested_employee, 
            context={'request': admin_response.wsgi_request}
        ).data
        mock_change.assert_called_with(self.tested_employee.uuid, self.expected_branch.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_change_branch_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.has_user_perm_to_company')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data
    
    def test_change_branch_for_anonymous_user(self):
        anonymous_response = self.anonymous_client.patch(self.url, data=self.patch_data)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data