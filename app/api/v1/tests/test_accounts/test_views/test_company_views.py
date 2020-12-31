from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts import factories as accounts_factories

from faker import Faker
import pytest


fake = Faker()


list_url_name = 'api_v1:accounts_companies-list'
detail_url_name = 'api_v1:accounts_companies-detail'
password_url_name = 'api_v1:accounts_companies-change-password'
deactivate_url_name = 'api_v1:accounts_companies-deactivate'

success_status = status.HTTP_200_OK
denied_status = status.HTTP_403_FORBIDDEN
unauth_status = status.HTTP_401_UNAUTHORIZED


# Тесты на действия
# Тесты на невалидные данные



@pytest.mark.django_db
class TestAccess():

    def test_access_for_admins(self, api_client, admin_user):
        expected_new_password = fake.password()
        company_account = accounts_factories.CompanyUserAccountModelFactory()
        api_client.force_authenticate(user=admin_user)
        list_response = api_client.get(reverse(list_url_name))
        detail_response = api_client.get(
            reverse(detail_url_name, kwargs={'uuid': company_account.uuid})
        )
        password_response = api_client.post(
            reverse(password_url_name, kwargs={'uuid': company_account.uuid}),
            data={'password1': expected_new_password, 'password2': expected_new_password}
        )
        deactivate_response = api_client.get(
            reverse(deactivate_url_name, kwargs={'uuid': company_account.uuid})
        )
        assert list_response.status_code == success_status
        assert detail_response.status_code == success_status
        assert password_response.status_code == success_status
        assert deactivate_response.status_code == success_status

    def test_access_for_companies(self, api_client, company_user):
        expected_new_password = fake.password()
        company_account = accounts_factories.CompanyUserAccountModelFactory()
        api_client.force_authenticate(user=company_user)
        list_response = api_client.get(reverse(list_url_name))
        detail_response = api_client.get(
            reverse(detail_url_name, kwargs={'uuid': company_account.uuid})
        )
        password_response = api_client.post(
            reverse(password_url_name, kwargs={'uuid': company_account.uuid}),
            data={'password1': expected_new_password, 'password2': expected_new_password}
        )
        deactivate_response = api_client.get(
            reverse(deactivate_url_name, kwargs={'uuid': company_account.uuid})
        )
        assert list_response.status_code == denied_status
        assert detail_response.status_code == denied_status
        assert password_response.status_code == denied_status
        assert deactivate_response.status_code == denied_status

    def test_access_for_employees(self, api_client, employee_user):
        expected_new_password = fake.password()
        company_account = accounts_factories.CompanyUserAccountModelFactory()
        api_client.force_authenticate(user=employee_user)
        list_response = api_client.get(reverse(list_url_name))
        detail_response = api_client.get(
            reverse(detail_url_name, kwargs={'uuid': company_account.uuid})
        )
        password_response = api_client.post(
            reverse(password_url_name, kwargs={'uuid': company_account.uuid}),
            data={'password1': expected_new_password, 'password2': expected_new_password}
        )
        deactivate_response = api_client.get(
            reverse(deactivate_url_name, kwargs={'uuid': company_account.uuid})
        )
        assert list_response.status_code == denied_status
        assert detail_response.status_code == denied_status
        assert password_response.status_code == denied_status
        assert deactivate_response.status_code == denied_status

    def test_access_for_anonymous(self, api_client):
        expected_new_password = fake.password()
        company_account = accounts_factories.CompanyUserAccountModelFactory()
        list_response = api_client.get(reverse(list_url_name))
        detail_response = api_client.get(
            reverse(detail_url_name, kwargs={'uuid': company_account.uuid})
        )
        password_response = api_client.post(
            reverse(password_url_name, kwargs={'uuid': company_account.uuid}),
            data={'password1': expected_new_password, 'password2': expected_new_password}
        )
        deactivate_response = api_client.get(
            reverse(deactivate_url_name, kwargs={'uuid': company_account.uuid})
        )
        assert list_response.status_code == unauth_status
        assert detail_response.status_code == unauth_status
        assert password_response.status_code == unauth_status
        assert deactivate_response.status_code == unauth_status


@pytest.mark.django_db
class TestChangePassword():

    def test_change_password_by_patch(self, api_client, admin_user):
        """
        Тест на попытку смены пароля напрямую через метод патч вьюсета.
        """
        expected_new_password = fake.password()
        expected_response_json = {
            'password': ['Для изменения пароля используйте функцию сброса пароля']
        }
        company_account = accounts_factories.CompanyUserAccountModelFactory()
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            reverse(detail_url_name, kwargs={'uuid': company_account.uuid}),
            data={'password': expected_new_password}
        )
        company_account.refresh_from_db()
        assert not check_password(expected_new_password, company_account.password)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response_json