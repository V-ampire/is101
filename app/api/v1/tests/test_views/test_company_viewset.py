from django.urls import reverse

from rest_framework import status

from company import factories as company_factories
from company.models import Company

from api.v1.companies import serializers

import factory
import pytest


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
    def test_access_to_company_for_not_company_user(self, api_client, company_user):
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
    def test_access_to_company_for_company_user(self, api_client):
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
    def test_access_to_companies_list_for_unauthed(self, api_client):
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
    content_type = 'application/json'

    @pytest.mark.django_db
    def test_create_company_by_admin(self, api_client, admin_user):
        """
        Тест на создание юрлица админом.
        """
        expected_status = status.HTTP_201_CREATED
        api_client.force_authenticate(user=admin_user)
        data = factory.build(dict, FACTORY_CLASS=company_factories.CompanyFactory)
        response = api_client.post(self.url, data=data, content_type=self.content_type)
        import pdb; pdb.set_trace()
