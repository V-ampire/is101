from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework import status

from accounts.factories import EmployeeUserAccountModelFactory

from companies.factories import EmployeeProfileFactory

from api.v1.tests.base import BaseViewSetTest

from api.v1.accounts.serializers import EmployeeUserAccountSerializer

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestViewSet(BaseViewSetTest):

    app_name = 'api_v1'
    url_basename = 'account-employees'

    def setup_method(self, method):
        super().setup_method(method)
        self.tested_user = EmployeeUserAccountModelFactory.create()

    

