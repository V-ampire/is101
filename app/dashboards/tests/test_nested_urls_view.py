from django.test import Client
from django.urls import reverse

import pytest


client = Client()


@pytest.mark.django_db
def test_set_urls_in_cookie(admin_user):
    client.force_login(admin_user)
    response = client.get('/dashboards/admin/companies/124546344/')
    import pdb; pdb.set_trace()
