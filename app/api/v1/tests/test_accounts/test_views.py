from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from faker import Faker
import pytest


fake = Faker()

# Тесты на доступ
# Тест на смену пароля
# Тесты на доступ к действиям
# Тесты на действия
# Тесты на невалидные данные


accounts_list_url = reverse('api_v1:accounts')



@pytest.mark.django_db
class TestAccess():

    success_status = status.HTTP_200_OK
    denied_status = status.HTTP_403_FORBIDDEN
    unauth_status = status.HTTP_401_UNAUTHORIZED

    def test_access_to_list(self, api_client, admin_user, company_user, employee_user):
        api_client.force_authenticate(user=admin_user)



def test_access_to_change_passsword_for_admin(api_client, admin_user, company_user):
    """
    Тест на доступ к изменению пароля.
    Доступ только у админов.
    """
    url = reverse('api_v1:change_password', kwargs={'pk': company_user.pk})
    api_client.force_authenticate(user=admin_user)
    expected_password = fake.password()
    tested_data = {
        'password1': expected_password,
        'password2': expected_password,
    }
    response = api_client.post(url, data=tested_data)
    company_user.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert check_password(expected_password, company_user.password)


@pytest.mark.django_db
def test_access_to_change_passsword_for_admin_fail(api_client, admin_user, company_user):
    """
    Тест на доступ к изменению пароля.
    Доступ только у админов.
    """
    url = reverse('api_v1:change_password', kwargs={'pk': company_user.pk})
    api_client.force_authenticate(user=admin_user)
    expected_password = 'qwerty'
    expected_response = {'password1': [
        'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.', 
        'Введённый пароль слишком широко распространён.'
    ]}
    tested_data = {
        'password1': expected_password,
        'password2': expected_password,
    }
    response = api_client.post(url, data=tested_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response
    assert not check_password(expected_password, company_user.password)
    

@pytest.mark.django_db
def test_access_to_change_passsword_for_company(api_client, company_user):
    """
    Тест на доступ к изменению пароля с учетки юрлица.
    Доступ запрещен
    """
    url = reverse('api_v1:change_password', kwargs={'pk': company_user.pk})
    api_client.force_authenticate(user=company_user)
    expected_password = fake.password()
    expected_response = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
    tested_data = {
        'password1': expected_password,
        'password2': expected_password,
    }
    response = api_client.post(url, data=tested_data)
    company_user.refresh_from_db()
    assert not check_password(expected_password, company_user.password)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == expected_response


@pytest.mark.django_db
def test_access_to_change_passsword_for_company(api_client, employee_user):
    """
    Тест на доступ к изменению пароля с учетки работника.
    Доступ запрещен
    """
    url = reverse('api_v1:change_password', kwargs={'pk': employee_user.pk})
    api_client.force_authenticate(user=employee_user)
    expected_password = fake.password()
    expected_response = {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
    tested_data = {
        'password1': expected_password,
        'password2': expected_password,
    }
    response = api_client.post(url, data=tested_data)
    employee_user.refresh_from_db()
    assert not check_password(expected_password, employee_user.password)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == expected_response