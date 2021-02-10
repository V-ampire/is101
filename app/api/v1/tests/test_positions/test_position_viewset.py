from django.urls import reverse
from django.conf import settings

from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory, AdminUserAccountModelFactory, EmployeeUserAccountModelFactory

from core.models import Statuses

from companies.factories import PositionFactory
from companies.models import Position

from api.v1.positions.serializers import PositionSerializer

from api.v1.tests.base import BaseViewSetTest

from factory_generator import generate_to_dict, generate_to_db
import pytest
from faker import Faker


fake = Faker()

@pytest.mark.django_db
class TestListAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.url = self.get_action_url('list')

    def test_permission_for_admin(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_permission_for_company(self, mocker):
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyUser.has_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_list_response_for_permitted(self, mocker):
        PositionFactory.create_batch(5, status=Statuses.ARCHIVED)
        PositionFactory.create_batch(5, status=Statuses.WORKS)
        mock_has_perm = mocker.patch('api.v1.permissions.IsCompanyUser.has_permission')
        mock_has_perm.return_value = True
        company_response = self.company_client.get(self.url)
        expected_data = PositionSerializer(
            Position.objects.filter(status=Statuses.WORKS), 
            many=True, 
            context={'request': company_response.wsgi_request}
        ).data
        assert company_response.status_code == status.HTTP_200_OK
        assert company_response.json() == expected_data

    def test_list_response_for_admin(self, mocker):
        generate_to_db(PositionFactory, quantity=5, status=Statuses.ARCHIVED)
        generate_to_db(PositionFactory, quantity=5, status=Statuses.WORKS)
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = PositionSerializer(
            Position.objects.all(), 
            many=True, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_list_response_for_forbidden(self, mocker):
        mock_has_perm_admin = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm_admin.return_value = False
        mock_has_perm_company = mocker.patch('api.v1.permissions.IsCompanyUser.has_permission')
        mock_has_perm_company.return_value = False
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
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_position = PositionFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_position.uuid)

    def test_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        assert mock_has_perm.call_count == 1

    def test_retrieve_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.get(self.url)
        expected_data = PositionSerializer(
            self.tested_position, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data

    def test_retrive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
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
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.create_data = generate_to_dict(PositionFactory)
        self.url = self.get_action_url('list')

    def test_create_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        assert mock_has_perm.call_count == 1

    def test_create_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.post(self.url, data=self.create_data)
        expected_position = Position.objects.get(**self.create_data)
        expected_data = PositionSerializer(
            expected_position, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_201_CREATED
        assert admin_response.json() == expected_data

    def test_create_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
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
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.patch_data = {
            'title': fake.job()
        }
        self.tested_position = PositionFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_position.uuid)

    def test_patch_permisiion(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        assert mock_has_perm.call_count == 1

    def test_patch_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url, data=self.patch_data)
        self.tested_position.refresh_from_db()
        expected_data = PositionSerializer(
            self.tested_position, 
            context={'request': admin_response.wsgi_request}
        ).data
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == expected_data
        assert self.tested_position.title == self.patch_data['title']

    def test_patch_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
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
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_position = PositionFactory.create()
        self.url = self.get_action_url('detail', uuid=self.tested_position.uuid)

    def test_destroy_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        mock_has_perm.call_count == 1

    def test_destroy_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.delete(self.url)
        assert admin_response.status_code == status.HTTP_204_NO_CONTENT
        assert not Position.objects.filter(uuid=self.tested_position.uuid).exists()

    def test_destroy_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        admin_response = self.admin_client.delete(self.url)
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_destroy_for_anonymous_user(self, mocker):
        anonymous_response = self.anonymous_client.delete(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data


@pytest.mark.django_db
class TestToArchiveAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_position = PositionFactory.create()
        self.url = self.get_action_url('to-archive', uuid=self.tested_position.uuid)
        self.expected_data = {'status': 'Должность переведена в архив.'}

    def test_to_archive_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_to_archive_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_archive = mocker.patch('api.v1.positions.views.utils.position_to_archive')
        admin_response = self.admin_client.patch(self.url)
        mock_to_archive.assert_called_with(self.tested_position.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_archive_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        mock_to_archive = mocker.patch('api.v1.positions.views.utils.position_to_archive')
        admin_response = self.admin_client.patch(self.url)
        assert mock_to_archive.call_count == 0
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_to_archive_for_anonymous_user(self, mocker):
        mock_to_archive = mocker.patch('api.v1.positions.views.utils.position_to_archive')
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
        assert mock_to_archive.call_count == 0


@pytest.mark.django_db
class TestToWorkAction(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'positions'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_position = PositionFactory.create()
        self.url = self.get_action_url('to-work', uuid=self.tested_position.uuid)
        self.expected_data = {'status': 'Должность в рабочем статусе.'}

    def test_to_work_permission(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        admin_response = self.admin_client.patch(self.url)
        mock_has_perm.call_count == 1

    def test_to_work_for_permitted(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = True
        mock_to_work = mocker.patch('api.v1.positions.views.utils.position_to_work')
        admin_response = self.admin_client.patch(self.url)
        mock_to_work.assert_called_with(self.tested_position.uuid)
        assert admin_response.status_code == status.HTTP_200_OK
        assert admin_response.json() == self.expected_data

    def test_to_work_for_forbidden(self, mocker):
        mock_has_perm = mocker.patch('api.v1.positions.views.IsAdminUser.has_permission')
        mock_has_perm.return_value = False
        mock_to_work = mocker.patch('api.v1.positions.views.utils.position_to_work')
        admin_response = self.admin_client.patch(self.url)
        assert mock_to_work.call_count == 0
        assert admin_response.status_code == status.HTTP_403_FORBIDDEN
        assert admin_response.json() == self.forbidden_data

    def test_to_work_for_anonymous_user(self, mocker):
        mock_to_work = mocker.patch('api.v1.positions.views.utils.position_to_work')
        anonymous_response = self.anonymous_client.patch(self.url)
        assert anonymous_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert anonymous_response.json() == self.unauth_data
        assert mock_to_work.call_count == 0

    