from rest_framework.test import APIClient

from django.urls import reverse

from accounts import factories

from collections import namedtuple
from factory_generator import generate_to_dict
import json
import os
import pytest


ActionConfig = namedtuple('ActionConfig', [
        'action',
        'method',
        'status_code',
        'data',
        'user'
    ])


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



class ViewsetTest():
    """
    Класс для тестирования вьюсетов.
    """
    actions_config = None
    viewset = None
    obj_factory_class = None
    app_name = 'api_v1'
    url_basename = 'company-branches'
    create_reports = False
    reports_path = None      

    def get_client(self):
        return APIClient()

    def get_action_url(self, action, *args, **kwargs):
        url = f'{self.app_name}:{self.url_basename}-{action}'
        return reverse(url, args=args, kwargs=kwargs)

    def get_object(self):
        return self.obj_factory_class()

    def test_viewset_actions(self):
        for config in self.actions_config:
            self._test_action(config)

    def save_action_report(self, action, report):
        file_name = f'{cls.viewset}-{action}.json'
        with open(os.path.join(self.reports_path, file_name), 'w') as fp:
            json.dump(report, fp, ensure_ascii=False, indent=4)

    def _test_action(self, config):
        client = self.get_client()
        obj = self.get_object()
        url = get_action_url(config.action, uuid=obj.uuid)
        expected_status = config.status_code
        try:
            data_getter = getattr(self, f'get_{config.action}_data')
            data = data_getter()
        except AttributeError:
            data = config.data
        if config.user:
            client.force_authenticate(user=config.user)
        method = getattr(client, config.method)
        response = method(url, data=data)
        if self.create_reports:
            report = {}
            report['request'] = {
                'url': url,
                'data': data,
                'user_role': user.role
            }
            report['response'] = {
                'status_code': response.status_code,
                'data': response.json()
            }

        assert response.status_code == expected_status
        
