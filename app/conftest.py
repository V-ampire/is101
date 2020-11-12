from rest_framework.test import APIClient

import pytest


pytest_plugins = [
    "accounts.tests.fixtures",
    "company.tests.fixtures"
]


@pytest.fixture
def api_client():
   return APIClient()