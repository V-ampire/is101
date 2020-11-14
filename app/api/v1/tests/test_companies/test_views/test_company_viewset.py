from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import encode_multipart

from rest_framework import status

from accounts.factories import CompanyUserAccountModelFactory

from company import factories as company_factories
from company.models import Company

from api.v1.companies import serializers

from faker import Faker
import pytest


fake = Faker()


class TestListCompanies():
    """
    Тест для метода CompanyViewSet.list()
    """

    url = reverse('api_v1:company-list')
    serializer_class = serializers.CompanyListSerializer

    @pytest.mark.django_db
    def test_access_to_companies_list_for_admin(self, api_client, admin_user, 
                                                create_companies):
        """
        Тест на доступ и данные списка юр. лиц для админов.
        """
        create_companies(3)
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)

        expected_status = status.HTTP_200_OK
        expected_data = self.serializer_class(
            Company.objects.all(), many=True, context={'request': response.wsgi_request}
        ).data
        assert expected_data == response.json()
        assert expected_status == response.status_code
        
    @pytest.mark.django_db
    def test_access_to_companies_list_for_company(self, api_client, company_user, 
                                                    create_companies):
        """
        Тест на доступ и данные списка юр. лиц для юр.лиц.

        У юр. лиц нет доступа.
        """
        create_companies(3)
        api_client.force_authenticate(user=company_user)

        response = api_client.get(self.url)
        expected_status = status.HTTP_403_FORBIDDEN
        expected_data = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        assert expected_status == response.status_code
        assert expected_data == response.data

    @pytest.mark.django_db
    def test_access_to_companies_list_for_employee(self, api_client, employee_user, 
                                                    create_companies):
        """
        Тест на доступ и данные списка юр. лиц для работников.

        У работников нет доступа.
        """
        create_companies(3)
        api_client.force_authenticate(user=employee_user)

        response = api_client.get(self.url)
        expected_status = status.HTTP_403_FORBIDDEN
        expected_data = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        assert expected_status == response.status_code
        assert expected_data == response.data

    @pytest.mark.django_db
    def test_access_to_companies_list_for_unauthed(self, api_client, create_companies):
        """
        Тест на доступ и данные списка юр. лиц для неавторизованных запросов.

        Нет доступа.
        """
        create_companies(3)

        response = api_client.get(self.url)
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_data = {'detail': 'Учетные данные не были предоставлены.'}
        assert expected_status == response.status_code
        assert expected_data == response.data
    

class TestCompanyDetail():
    """
    Тест для метода CompanyViewSet.retrieve()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = reverse('api_v1:company-detail', args=[self.company.uuid])

    @pytest.mark.django_db
    def test_access_to_company_for_admin(self, api_client, admin_user):
        """
        Тест на доступ и данные юр. лица для админов.
        """
        serializer_class = serializers.CompanySerializerForAdmin
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)

        expected_status = status.HTTP_200_OK
        expected_data = serializer_class(
            Company.objects.get(pk=self.company.pk), 
            context={'request': response.wsgi_request}
        ).data
        assert expected_data == response.json()
        assert expected_status == response.status_code
        
    @pytest.mark.django_db
    def test_access_to_company_other_company_users(self, api_client, company_user):
        """
        Тест на доступ и данные юр. лица для других юр.лиц.

        У других юр. лиц нет доступа.
        """
        api_client.force_authenticate(user=company_user)
        response = api_client.get(self.url)
        expected_status = status.HTTP_403_FORBIDDEN
        expected_data = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        assert expected_status == response.status_code
        assert expected_data == response.data

    @pytest.mark.django_db
    def test_access_to_company_owner(self, api_client):
        """
        Тест на доступ и данные юр. лица для владельца.
        """
        serializer_class = serializers.CompanySerializerForOwner
        api_client.force_authenticate(user=self.company.user)
        response = api_client.get(self.url)

        expected_status = status.HTTP_200_OK
        expected_data = serializer_class(
            Company.objects.get(pk=self.company.pk), 
            context={'request': response.wsgi_request}
        ).data
        assert expected_data == response.json()
        assert expected_status == response.status_code

    @pytest.mark.django_db
    def test_access_to_companies_list_for_employee(self, api_client, employee_user):
        """
        Тест на доступ и данные юр. лица для работников.

        У работников нет доступа.
        """
        api_client.force_authenticate(user=employee_user)

        response = api_client.get(self.url)
        expected_status = status.HTTP_403_FORBIDDEN
        expected_data = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        assert expected_status == response.status_code
        assert expected_data == response.data

    @pytest.mark.django_db
    def test_access_to_companies_list_for_anonymous(self, api_client):
        """
        Тест на доступ и данные юр. лица для неавторизованных запросов.

        Нет доступа.
        """
        response = api_client.get(self.url)
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_data = {'detail': 'Учетные данные не были предоставлены.'}
        assert expected_status == response.status_code
        assert expected_data == response.data


class TestCompanyCreate():
    """
    Тест для метода CompanyViewSet.create()
    """
    url = reverse('api_v1:company-list')

    @pytest.mark.django_db
    def test_create_company_by_admin(self, api_client, admin_user, factory_as_dict):
        """
        Тест на создание юрлица админом.
        """
        expected_status = status.HTTP_201_CREATED
        api_client.force_authenticate(user=admin_user)
        factory_data = factory_as_dict(company_factories.CompanyFactory)
        user = factory_data['user']
        factory_data.update({'user.username': user.username, 'user.password': user.password})
        response = api_client.post(self.url, data=factory_data)
        assert response.status_code == expected_status
        assert get_user_model().company_objects.filter(username=user.username).exists()

    @pytest.mark.django_db
    def test_create_company_by_owner(self, api_client, company_user, factory_as_dict):
        """
        Тест на создание юрлица админом.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_response_data = {
            'detail': 'У вас недостаточно прав для выполнения данного действия.'
        }
        api_client.force_authenticate(user=company_user)
        factory_data = factory_as_dict(company_factories.CompanyFactory)
        user = factory_data['user']
        factory_data.update({'user.username': user.username, 'user.password': user.password})
        response = api_client.post(self.url, data=factory_data)
        assert response.status_code == expected_status
        assert response.json() == expected_response_data
        assert not get_user_model().company_objects.filter(username=user.username).exists()

    @pytest.mark.django_db
    def test_create_company_by_employee(self, api_client, employee_user, factory_as_dict):
        """
        Тест на создание юрлица админом.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_response_data = {
            'detail': 'У вас недостаточно прав для выполнения данного действия.'
        }
        api_client.force_authenticate(user=employee_user)
        factory_data = factory_as_dict(company_factories.CompanyFactory)
        user = factory_data['user']
        factory_data.update({'user.username': user.username, 'user.password': user.password})
        response = api_client.post(self.url, data=factory_data)
        assert response.status_code == expected_status
        assert response.json() == expected_response_data
        assert not get_user_model().company_objects.filter(username=user.username).exists()

    @pytest.mark.django_db
    def test_create_company_by_anonymous(self, api_client, factory_as_dict):
        """
        Тест на создание юрлица админом.
        """
        tested_username = 'anonymous'
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_response_data = {'detail': 'Учетные данные не были предоставлены.'}
        factory_data = factory_as_dict(company_factories.CompanyFactory)
        factory_data.update({'user.username': tested_username, 'user.password': 'test-password'})
        response = api_client.post(self.url, data=factory_data)
        assert response.status_code == expected_status
        assert response.json() == expected_response_data
        assert not get_user_model().company_objects.filter(username=tested_username).exists()


class TestCompanyPatch():
    """
    Тест для метода CompanyViewSet.partial_update()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = reverse('api_v1:company-detail', args=[self.company.uuid])

    @pytest.mark.django_db
    def test_update_username_by_admin(self, api_client, admin_user):
        """
        Тест на обновление поля username юрлица админом.
        """
        expected_status = status.HTTP_200_OK
        expected_username = fake.user_name()
        api_client.force_authenticate(user=admin_user)
        data = {'user.username': expected_username}
        response = api_client.patch(self.url, data=data)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert self.company.user.username == expected_username

    @pytest.mark.django_db
    def test_update_password_by_admin(self, api_client, admin_user):
        """
        Тест на обновление пароля юрлица админом.
        """
        expected_status = status.HTTP_400_BAD_REQUEST
        expected_password = fake.password()
        expected_response_data = {
            'user': ['Для изменения пароля используйте функцию сброса пароля']
        }
        api_client.force_authenticate(user=admin_user)
        data = {'user.password': expected_password}
        response = api_client.patch(self.url, data=data)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert response.json() == expected_response_data

    @pytest.mark.django_db
    def test_update_by_owner(self, api_client):
        """
        Тест на обновление юрлица самим юрлицом.
        """
        expected_status = status.HTTP_200_OK
        expected_title = fake.company()
        api_client.force_authenticate(user=self.company.user)
        data = {'title': expected_title}
        response = api_client.patch(self.url, data=data)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert self.company.title == expected_title

    @pytest.mark.django_db
    def test_update_by_other_company(self, api_client, company_user):
        """
        Тест на обновление юрлица другим юрлицом.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_title = fake.company()
        api_client.force_authenticate(user=company_user)
        data = {'title': expected_title}
        response = api_client.patch(self.url, data=data)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.title == expected_title

    @pytest.mark.django_db
    def test_update_by_other_anonymous(self, api_client):
        """
        Тест на обновление юрлица неавторизованным пользователем.
        """
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_title = fake.company()
        data = {'title': expected_title}
        response = api_client.patch(self.url, data=data)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.title == expected_title


class TestCompanyDestroy():
    """
    Тест для метода CompanyViewSet.destroy()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = reverse('api_v1:company-detail', args=[self.company.uuid])

    @pytest.mark.django_db
    def test_destroy_company_by_admin(self, api_client, admin_user):
        """
        Удаление юрлица админом.
        Одновременно удаляется учетная запись.
        """
        expected_status = status.HTTP_204_NO_CONTENT
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(self.url)
        assert response.status_code == expected_status
        assert not Company.objects.filter(pk=self.company.pk).exists()
        assert not get_user_model().objects.filter(pk=self.company.user.pk).exists()

    @pytest.mark.django_db
    def test_destroy_company_by_company(self, api_client, company_user):
        """
        Удаление юрлица юрлицом.
        Доступ запрещен.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        api_client.force_authenticate(user=company_user)
        response = api_client.delete(self.url)
        assert response.status_code == expected_status
        assert Company.objects.filter(pk=self.company.pk).exists()
        assert get_user_model().objects.filter(pk=self.company.user.pk).exists()

    @pytest.mark.django_db
    def test_destroy_company_by_employee(self, api_client, employee_user):
        """
        Удаление юрлица работником.
        Доступ запрещен.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        api_client.force_authenticate(user=employee_user)
        response = api_client.delete(self.url)
        assert response.status_code == expected_status
        assert Company.objects.filter(pk=self.company.pk).exists()
        assert get_user_model().objects.filter(pk=self.company.user.pk).exists()

    @pytest.mark.django_db
    def test_destroy_company_by_anonymous(self, api_client):
        """
        Удаление юрлица неавторизованным пользователем.
        Доступ запрещен.
        """
        expected_status = status.HTTP_401_UNAUTHORIZED
        api_client.force_authenticate()
        response = api_client.delete(self.url)
        assert response.status_code == expected_status
        assert Company.objects.filter(pk=self.company.pk).exists()
        assert get_user_model().objects.filter(pk=self.company.user.pk).exists()


class TestCompanyArchivate():
    """
    Тест действия CompanyViewSet.archivate()
    """
    def setup_method(self, method):
        self.company = company_factories.CompanyFactory()
        self.url = reverse('api_v1:company-archivate', args=[self.company.uuid])

    @pytest.mark.django_db
    def test_archivate_by_admin(self, api_client, admin_user):
        """
        Тест архивирования юрлица админом.
        """
        expected_status = status.HTTP_200_OK
        expected_company_status = Company.ARCHIVED
        expected_response_data = {
            'status': expected_company_status
        }
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert response.json() == expected_response_data
        assert self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_archivate_by_company(self, api_client, company_user):
        """
        Тест архивирования юрлица юрлицом.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_company_status = Company.ARCHIVED
        api_client.force_authenticate(user=company_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_archivate_by_employee(self, api_client, employee_user):
        """
        Тест архивирования юрлица работником.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_company_status = Company.ARCHIVED
        api_client.force_authenticate(user=employee_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_archivate_by_anonymous(self, api_client):
        """
        Тест архивирования юрлица работником.
        """
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_company_status = Company.ARCHIVED
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status


class TestCompanyActivate():
    """
    Тест действия CompanyViewSet.activate()
    """
    def setup_method(self, method):
        self.company = company_factories.ArchivedCompanyFactory()
        self.url = reverse('api_v1:company-activate', args=[self.company.uuid])

    @pytest.mark.django_db
    def test_activate_by_admin(self, api_client, admin_user):
        """
        Тест активации юрлица админом.
        """
        expected_status = status.HTTP_200_OK
        expected_company_status = Company.ACTIVE
        expected_response_data = {
            'status': expected_company_status
        }
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert response.json() == expected_response_data
        assert self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_activate_by_company(self, api_client, company_user):
        """
        Тест архивирования юрлица юрлицом.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_company_status = Company.ACTIVE
        api_client.force_authenticate(user=company_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_activate_by_employee(self, api_client, employee_user):
        """
        Тест архивирования юрлица работником.
        """
        expected_status = status.HTTP_403_FORBIDDEN
        expected_company_status = Company.ACTIVE
        api_client.force_authenticate(user=employee_user)
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status

    @pytest.mark.django_db
    def test_activate_by_anonymous(self, api_client):
        """
        Тест архивирования юрлица работником.
        """
        expected_status = status.HTTP_401_UNAUTHORIZED
        expected_company_status = Company.ACTIVE
        response = api_client.get(self.url)
        self.company.refresh_from_db()
        assert response.status_code == expected_status
        assert not self.company.status == expected_company_status

    















