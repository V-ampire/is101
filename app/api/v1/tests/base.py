from rest_framework.test import APIClient

from django.urls import reverse

from accounts import factories

from factory_generator import generate_to_dict
import json
import os
import pytest



class BaseViewSetTest():

    app_name = None
    url_basename = None

    def get_api_client(self, user=None):
        client = APIClient()
        if user:
            client.force_authenticate(user=user)
        return client

    def get_action_url(self, action, *args, **kwargs):
        url = f'{self.app_name}:{self.url_basename}-{action}'
        return reverse(url, args=args, kwargs=kwargs)

    def setup_method(self, method):
        self.admin_user = factories.AdminUserAccountModelFactory.create()
        self.company_user = factories.CompanyUserAccountModelFactory.create()
        self.employee_user = factories.EmployeeUserAccountModelFactory.create()
        self.admin_client = self.get_api_client(user=self.admin_user)
        self.company_client = self.get_api_client(user=self.company_user)
        self.employee_client = self.get_api_client(user=self.employee_user)
        self.anonymous_client = self.get_api_client()