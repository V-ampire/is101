from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.serializers import ValidationError

from accounts.factories import CompanyUserAccountModelFactory

from company import factories as company_factories
from company.models import Company

from api.v1.companies import serializers

from factory_generator.utils import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


success_status = status.HTTP_200_OK
created_status = status.HTTP_201_CREATED
denied_status = status.HTTP_403_FORBIDDEN
unauth_status = status.HTTP_401_UNAUTHORIZED
deleted_status = status.HTTP_204_NO_CONTENT

# Тесты на доступ
# Тест на попытку создать/изменить учетку через сериалайзер

def get_action_url(action, *args, **kwargs):
    url = f'api_v1:company-{action}'
    return reverse(url, args=args, kwargs=kwargs)    


@pytest.mark.django_db
class TestAccess():

    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()

        self.post_data = generate_to_dict(company_factories.CompanyFactory)
        self.post_data.pop('user')
        self.post_data.update({'user': CompanyUserAccountModelFactory().uuid})

        self.patch_data = generate_to_dict(company_factories.CompanyFactory)
        self.patch_data.pop('user')        


    def test_access_for_admins(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)

        list_response = api_client.get(get_action_url('list'))
        detail_response = api_client.get(get_action_url('detail', uuid=self.company.uuid))
        create_response = api_client.post(get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            get_action_url('detail', uuid=self.company.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(get_action_url('archivate', uuid=self.company.uuid))
        activate_response = api_client.get(get_action_url('activate', uuid=self.company.uuid))
        delete_response = api_client.delete(get_action_url('detail', uuid=self.company.uuid))

        assert list_response.status_code == success_status
        assert detail_response.status_code == success_status
        assert create_response.status_code == created_status
        assert patch_response.status_code == success_status
        assert archivate_response.status_code == success_status
        assert activate_response.status_code == success_status
        assert delete_response.status_code == deleted_status


    def test_access_for_company(self, api_client, company_user):
        api_client.force_authenticate(user=company_user)

        list_response = api_client.get(get_action_url('list'))
        detail_response = api_client.get(get_action_url('detail', uuid=self.company.uuid))
        create_response = api_client.post(get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            get_action_url('detail', uuid=self.company.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(get_action_url('archivate', uuid=self.company.uuid))
        activate_response = api_client.get(get_action_url('activate', uuid=self.company.uuid))

        delete_response = api_client.delete(get_action_url('detail', uuid=self.company.uuid))

        assert list_response.status_code == denied_status
        assert detail_response.status_code == denied_status
        assert create_response.status_code == denied_status
        assert patch_response.status_code == denied_status
        assert delete_response.status_code == denied_status
        assert archivate_response.status_code == denied_status
        assert activate_response.status_code == denied_status

    def test_access_for_employee(self, api_client, employee_user):
        api_client.force_authenticate(user=employee_user)

        list_response = api_client.get(get_action_url('list'))
        detail_response = api_client.get(get_action_url('detail', uuid=self.company.uuid))
        create_response = api_client.post(get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            get_action_url('detail', uuid=self.company.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(get_action_url('archivate', uuid=self.company.uuid))
        activate_response = api_client.get(get_action_url('activate', uuid=self.company.uuid))

        delete_response = api_client.delete(get_action_url('detail', uuid=self.company.uuid))

        assert list_response.status_code == denied_status
        assert detail_response.status_code == denied_status
        assert create_response.status_code == denied_status
        assert patch_response.status_code == denied_status
        assert delete_response.status_code == denied_status
        assert archivate_response.status_code == denied_status
        assert activate_response.status_code == denied_status
    
    def test_access_for_anonymous(self, api_client):

        list_response = api_client.get(get_action_url('list'))
        detail_response = api_client.get(get_action_url('detail', uuid=self.company.uuid))
        create_response = api_client.post(get_action_url('list'), data=self.post_data)
        patch_response = api_client.patch(
            get_action_url('detail', uuid=self.company.uuid), data=self.patch_data
        )
        archivate_response = api_client.get(get_action_url('archivate', uuid=self.company.uuid))
        activate_response = api_client.get(get_action_url('activate', uuid=self.company.uuid))

        delete_response = api_client.delete(get_action_url('detail', uuid=self.company.uuid))

        assert list_response.status_code == unauth_status
        assert detail_response.status_code == unauth_status
        assert create_response.status_code == unauth_status
        assert patch_response.status_code == unauth_status
        assert delete_response.status_code == unauth_status
        assert archivate_response.status_code == unauth_status
        assert activate_response.status_code == unauth_status

    def test_access_for_permitted(self, api_client):

        for permitted_user in self.company.permitted_users:

            api_client.force_authenticate(user=permitted_user)

            list_response = api_client.get(get_action_url('list'))
            detail_response = api_client.get(get_action_url('detail', uuid=self.company.uuid))
            create_response = api_client.post(get_action_url('list'), data=self.post_data)
            patch_response = api_client.patch(
                get_action_url('detail', uuid=self.company.uuid), data=self.patch_data
            )
            archivate_response = api_client.get(get_action_url('archivate', uuid=self.company.uuid))
            activate_response = api_client.get(get_action_url('activate', uuid=self.company.uuid))

            delete_response = api_client.delete(get_action_url('detail', uuid=self.company.uuid))

            assert list_response.status_code == denied_status
            assert detail_response.status_code == success_status
            assert create_response.status_code == denied_status
            assert patch_response.status_code == success_status
            assert delete_response.status_code == denied_status
            assert archivate_response.status_code == denied_status
            assert activate_response.status_code == denied_status


@pytest.mark.django_db
class TestListCompanies():
    """
    Тест для метода CompanyViewSet.list()
    """

    serializer_class = serializers.CompanyListSerializer

    def test_access_to_companies_list_for_admin(self, api_client, admin_user, 
                                                create_companies):
        """
        Тест на доступ и данные списка юр. лиц для админов.
        """
        create_companies(3)
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(get_action_url('list'))

        expected_status = success_status
        expected_data = self.serializer_class(
            Company.objects.all().order_by('-status'), many=True, context={'request': response.wsgi_request}
        ).data
        assert expected_data == response.json()
        assert expected_status == response.status_code
        

@pytest.mark.django_db
class TestCompanyDetail():
    """
    Тест для метода CompanyViewSet.retrieve()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = get_action_url('detail', uuid=self.company.uuid)

    def test_access_to_company_for_admin(self, api_client, admin_user):
        """
        Тест на доступ и данные юр. лица для админов.
        """
        serializer_class = serializers.CompanyDetailSerializerForAdmin
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)

        expected_status = success_status
        expected_data = serializer_class(
            Company.objects.get(pk=self.company.pk), 
            context={'request': response.wsgi_request}
        ).data
        assert expected_data == response.json()
        assert expected_status == response.status_code
        
    def test_access_to_company_permitted(self, api_client):
        """
        Тест на доступ и данные юр. лица для владельца.
        """
        serializer_class = serializers.CompanySerializerForPermitted

        for permitted_user in self.company.permitted_users:
            api_client.force_authenticate(user=permitted_user)
            response = api_client.get(self.url)

            expected_status = success_status
            expected_data = serializer_class(
                Company.objects.get(pk=self.company.pk), 
                context={'request': response.wsgi_request}
            ).data
            assert expected_data == response.json()
            assert expected_status == response.status_code

            assert expected_data == response.data


@pytest.mark.django_db
class TestCompanyCreate():
    """
    Тест для метода CompanyViewSet.create()
    """
    url = get_action_url('list')

    def test_create_company_by_admin(self, api_client, admin_user, company_user):
        """
        Тест на создание юрлица админом.
        """
        api_client.force_authenticate(user=admin_user)
        post_data = generate_to_dict(company_factories.CompanyFactory)
        post_data.pop('user')
        post_data.update({'user': company_user.uuid})        
        response = api_client.post(self.url, data=post_data)
        assert response.status_code == created_status
        assert Company.objects.filter(title=post_data['title']).exists()

    def test_create_with_invalid_user(self, api_client, admin_user, company_user):
        expected_response = {'user': ['Учетная запись не зарегистрирована']}
        api_client.force_authenticate(user=admin_user)
        post_data = generate_to_dict(company_factories.CompanyFactory)
        post_data['user'] = fake.uuid4()
        response = api_client.post(self.url, data=post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

    def test_create_company_validate_user(self, api_client, admin_user, mocker,
                                                company_user):
        api_client.force_authenticate(user=admin_user)
        mock_validate = mocker.patch(
            'api.v1.companies.validators.validate_user_data_for_create')
        mock_validate.return_value = company_user
        api_client.force_authenticate(user=admin_user)
        post_data = generate_to_dict(company_factories.CompanyFactory)
        post_data.pop('user')
        post_data.update({'user': company_user.uuid})
        response = api_client.post(self.url, data=post_data)
        assert response.status_code == created_status
        mock_validate.assert_called_with(uuid=company_user.uuid)


@pytest.mark.django_db
class TestCompanyPatch():
    """
    Тест для метода CompanyViewSet.partial_update()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = get_action_url('detail', uuid=self.company.uuid)
        self.patch_data = generate_to_dict(company_factories.CompanyFactory)
        self.patch_data.pop('user') 

    def test_success_update_company_by_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        expected_uuid = self.company.uuid
        response = api_client.patch(self.url, data=self.patch_data)
        tested_company = Company.objects.get(title=self.patch_data['title'])
        assert response.status_code == success_status
        assert tested_company.uuid == expected_uuid

    def test_success_update_company_by_permitted(self, api_client):
        for permitted_user in self.company.permitted_users:
            api_client.force_authenticate(user=permitted_user)
            expected_uuid = self.company.uuid
            response = api_client.patch(self.url, data=self.patch_data)
            tested_company = Company.objects.get(title=self.patch_data['title'])
            assert response.status_code == success_status
            assert tested_company.uuid == expected_uuid

    def test_disable_patch_user_by_admin(self, api_client, admin_user, company_user):
        api_client.force_authenticate(user=admin_user)
        expected_user_uuid = self.company.user.uuid
        response = api_client.patch(self.url, data={'user': company_user.uuid})
        self.company.refresh_from_db()
        assert response.status_code == success_status
        assert self.company.user.uuid == expected_user_uuid
    
    def test_disable_patch_user_by_permitted(self, api_client, admin_user, company_user):
        expected_user_uuid = self.company.user.uuid
        for permitted_user in self.company.permitted_users:
            api_client.force_authenticate(user=permitted_user)
            response = api_client.patch(self.url, data={'user': company_user.uuid})
            self.company.refresh_from_db()
            assert response.status_code == success_status
            assert self.company.user.uuid == expected_user_uuid


@pytest.mark.django_db
class TestCompanyDestroy():
    """
    Тест для метода CompanyViewSet.destroy()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = get_action_url('detail', uuid=self.company.uuid)

    def test_destroy_company_by_admin(self, api_client, admin_user):
        """
        Удаление юрлица админом.
        Одновременно удаляется учетная запись.
        """
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(self.url)
        assert response.status_code == deleted_status
        assert not Company.objects.filter(pk=self.company.pk).exists()
        assert not get_user_model().objects.filter(pk=self.company.user.pk).exists()


@pytest.mark.django_db
class TestCompanyArchivate():
    """
    Тест действия CompanyViewSet.archivate()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = get_action_url('archivate', uuid=self.company.uuid)

    def test_archivate_by_admin(self, api_client, admin_user):
        """
        Тест архивирования юрлица админом.
        """
        expected_company_status = Company.ARCHIVED
        expected_response_data = {
            'status': 'ok'
        }
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == success_status
        assert response.json() == expected_response_data
        assert self.company.status == expected_company_status


@pytest.mark.django_db
class TestCompanyActivate():
    """
    Тест действия CompanyViewSet.activate()
    """
    def setup_method(self, method):
        self.company = company_factories.ArchivedCompanyFactory()
        self.url = get_action_url('activate', uuid=self.company.uuid)

    def test_activate_by_admin(self, api_client, admin_user):
        """
        Тест активации юрлица админом.
        """
        expected_company_status = Company.ACTIVE
        expected_response_data = {
            'status': 'ok'
        }
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == success_status
        assert response.json() == expected_response_data
        assert self.company.status == expected_company_status










