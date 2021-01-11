from django.urls import reverse

from company import factories as company_factories

from faker import Faker
import pytest


success_status = status.HTTP_200_OK
created_status = status.HTTP_201_CREATED
denied_status = status.HTTP_403_FORBIDDEN
unauth_status = status.HTTP_401_UNAUTHORIZED
deleted_status = status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestAccess():

    obj_factory_class = PositionFactory
    user_factory_class = CompanyUserAccountModelFactory
    app_name = 'api_v1'
    url_basename = 'company-branches'

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

        assert list_response.status_code == denied_status
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