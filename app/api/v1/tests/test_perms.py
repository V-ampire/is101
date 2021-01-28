from django.urls import reverse

from factory_generator import generate_to_db

from accounts.factories import EmployeeUserAccountModelFactory

import pytest


@pytest.mark.django_db
def test(api_client, admin_user):
    employees = generate_to_db(EmployeeUserAccountModelFactory)
    api_client.force_authenticate(user=admin_user)
    url = reverse('api_v1:account-employees-activate', kwargs={'uuid': employees[0].uuid})
    response = api_client.patch(url)