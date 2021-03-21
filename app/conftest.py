from rest_framework.test import APIClient

import factory
import pytest


pytest_plugins = [
    "accounts.tests.fixtures",
]

@pytest.fixture
def api_client():
   return APIClient()