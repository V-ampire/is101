from django.urls import reverse
from django.conf import settings

from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory, AdminUserAccountModelFactory, EmployeeUserAccountModelFactory

from company.factories import PositionFactory
from company.models import Position

from api.v1.positions.serializers import PositionSerializer

from api.v1.tests.base import BaseViewsetTest, ActionConfig

from factory_generator import generate_to_dict
import pytest
import os


success_status = status.HTTP_200_OK
created_status = status.HTTP_201_CREATED
denied_status = status.HTTP_403_FORBIDDEN
unauth_status = status.HTTP_401_UNAUTHORIZED
deleted_status = status.HTTP_204_NO_CONTENT

admin_user = AdminUserAccountModelFactory()
company_user = CompanyUserAccountModelFactory()
employee_user = EmployeeUserAccountModelFactory()


class TestViewSet(BaseViewsetTest):
    actions_config = [
        ActionConfig('detail', 'get', success_status, data=None, user=admin_user)
    ]
    obj_factory_class = PositionFactory
    app_name = 'api_v1'
    url_basename = 'position'
    create_reports = True
    reports_path = os.path.join(settings.BASE_DIR, 'api/v1/docs/positions')


@pytest.mark.django_db
class TestAccess():

    obj_factory_class = PositionFactory
    user_factory_class = CompanyUserAccountModelFactory
    app_name = 'api_v1'
    url_basename = 'position'

    def get_action_url(self, action, *args, **kwargs):
        url = f'{self.app_name}:{self.url_basename}-{action}'
        return reverse(url, args=args, kwargs=kwargs) 

    def setup_method(self, method):
        self.obj = self.obj_factory_class()

        self.post_data = generate_to_dict(self.obj_factory_class)
        self.patch_data = generate_to_dict(self.obj_factory_class)

    def test_access_for_admins(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)

        list_response = api_client.get(self.get_action_url('list'))
        detail_response = api_client.get(self.get_action_url('detail', uuid=self.obj.uuid))
        create_response = api_client.post(self.get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            self.get_action_url('detail', uuid=self.obj.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(self.get_action_url('archivate', uuid=self.obj.uuid))
        activate_response = api_client.get(self.get_action_url('activate', uuid=self.obj.uuid))
        delete_response = api_client.delete(self.get_action_url('detail', uuid=self.obj.uuid))

        assert list_response.status_code == success_status
        assert detail_response.status_code == success_status
        assert create_response.status_code == created_status
        assert patch_response.status_code == success_status
        assert archivate_response.status_code == success_status
        assert activate_response.status_code == success_status
        assert delete_response.status_code == deleted_status

    def test_access_for_company(self, api_client, company_user):
        api_client.force_authenticate(user=company_user)

        list_response = api_client.get(self.get_action_url('list'))
        detail_response = api_client.get(self.get_action_url('detail', uuid=self.obj.uuid))
        create_response = api_client.post(self.get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            self.get_action_url('detail', uuid=self.obj.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(self.get_action_url('archivate', uuid=self.obj.uuid))
        activate_response = api_client.get(self.get_action_url('activate', uuid=self.obj.uuid))

        delete_response = api_client.delete(self.get_action_url('detail', uuid=self.obj.uuid))

        assert list_response.status_code == success_status
        assert detail_response.status_code == denied_status
        assert create_response.status_code == denied_status
        assert patch_response.status_code == denied_status
        assert delete_response.status_code == denied_status
        assert archivate_response.status_code == denied_status
        assert activate_response.status_code == denied_status

    def test_access_for_employee(self, api_client, employee_user):
        api_client.force_authenticate(user=employee_user)

        list_response = api_client.get(self.get_action_url('list'))
        detail_response = api_client.get(self.get_action_url('detail', uuid=self.obj.uuid))
        create_response = api_client.post(self.get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            self.get_action_url('detail', uuid=self.obj.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(self.get_action_url('archivate', uuid=self.obj.uuid))
        activate_response = api_client.get(self.get_action_url('activate', uuid=self.obj.uuid))

        delete_response = api_client.delete(self.get_action_url('detail', uuid=self.obj.uuid))

        assert list_response.status_code == denied_status
        assert detail_response.status_code == denied_status
        assert create_response.status_code == denied_status
        assert patch_response.status_code == denied_status
        assert delete_response.status_code == denied_status
        assert archivate_response.status_code == denied_status
        assert activate_response.status_code == denied_status
    
    def test_access_for_anonymous(self, api_client):
        list_response = api_client.get(self.get_action_url('list'))
        detail_response = api_client.get(self.get_action_url('detail', uuid=self.obj.uuid))
        create_response = api_client.post(self.get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            self.get_action_url('detail', uuid=self.obj.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(self.get_action_url('archivate', uuid=self.obj.uuid))
        activate_response = api_client.get(self.get_action_url('activate', uuid=self.obj.uuid))

        delete_response = api_client.delete(self.get_action_url('detail', uuid=self.obj.uuid))

        assert list_response.status_code == unauth_status
        assert detail_response.status_code == unauth_status
        assert create_response.status_code == unauth_status
        assert patch_response.status_code == unauth_status
        assert delete_response.status_code == unauth_status
        assert archivate_response.status_code == unauth_status
        assert activate_response.status_code == unauth_status


@pytest.mark.django_db
class TestListPositions():

    serializer_class = PositionSerializer
    app_name = 'api_v1'
    url_basename = 'position'

    def get_action_url(self, action, *args, **kwargs):
        url = f'{self.app_name}:{self.url_basename}-{action}'
        return reverse(url, args=args, kwargs=kwargs) 

    def test_list_positions_for_admins(self, api_client, admin_user):
        """
        Тест на получение списка админами.
        """
        active_positions = [PositionFactory(status=Position.ACTIVE) for i in range(3)]
        archive_positions = [PositionFactory(status=Position.ARCHIVED) for i in range(3)]       
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.get_action_url('list'))
        expected_data = self.serializer_class(
            Position.objects.all(),
            many=True,
            context={'request': response.wsgi_request}
        ).data
        import pdb; pdb.set_trace()
        assert expected_data == response.json()


    def test_get_position_list_by_company(self, api_client, company_user):
        """
        Тест на получение списка юрлицом.
        Юрлицо имеет доступ только к списку активных должностей.
        """
        active_positions = [PositionFactory(status=Position.ACTIVE) for i in range(3)]
        archive_positions = [PositionFactory(status=Position.ARCHIVED) for i in range(3)]
        url = reverse('api_v1:position-list')
        api_client.force_authenticate(user=company_user)
        response = api_client.get(self.get_action_url('list'))

        expected_data = PositionSerializer(
            Position.objects.filter(status=Position.ACTIVE), 
            many=True, 
            context={'request': response.wsgi_request}
        ).data
        import pdb; pdb.set_trace()
        assert expected_data == response.json()

