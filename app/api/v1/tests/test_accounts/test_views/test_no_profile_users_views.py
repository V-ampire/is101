from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from accounts import factories

from companies import factories as company_factories

from api.v1.accounts.serializers import ReadOnlyUserAccountSerializer

from faker import Faker
import pytest


list_view_url = reverse('api_v1:accounts-no_profiles')
count_view_url = reverse('api_v1:accounts-no_profiles-count')


@pytest.mark.django_db
def test_permissions(api_client, mocker):
    mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
    mock_has_perm.return_value = True
    response = api_client.get(list_view_url)
    assert mock_has_perm.call_count == 1


@pytest.mark.django_db
def test_response(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    company_factories.CompanyProfileFactory.create_batch(3)
    company_factories.EmployeeProfileFactory.create_batch(3)
    expected_users = []
    expected_users.extend(factories.CompanyUserAccountModelFactory.create_batch(3))
    expected_users.extend(factories.EmployeeUserAccountModelFactory.create_batch(3))
    response = api_client.get(list_view_url)
    expected_response = ReadOnlyUserAccountSerializer(
        expected_users, many=True, context={'request': response.wsgi_request}
    ).data
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_permissions_for_count_view(api_client, mocker):
    mock_has_perm = mocker.patch('api.v1.companies.views.IsAdminUser.has_permission')
    mock_has_perm.return_value = True
    response = api_client.get(count_view_url)
    assert mock_has_perm.call_count == 1


@pytest.mark.django_db
def test_count_response(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    company_factories.CompanyProfileFactory.create_batch(3)
    company_factories.EmployeeProfileFactory.create_batch(3)
    expected_users = []
    expected_users.extend(factories.CompanyUserAccountModelFactory.create_batch(3))
    expected_users.extend(factories.EmployeeUserAccountModelFactory.create_batch(3))
    response = api_client.get(count_view_url)
    expected_response = {'count': len(expected_users)}
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


