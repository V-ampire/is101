from rest_framework.test import APIClient

from django.urls import reverse

from factory_generator import generate_to_dict
import json
import os
import pytest


class DocClient():

    def __init__(self, registry):
        self.client = APIClient()
        self.registry = registry

    def get(self, path, data=None, follow=False, **extra):
        self.registry['get']['request'] = {
            'path': path, 
            'data': data
        }
        response = self.client.get(path, data=None, follow=False, **extra)
        self.registry['get']['response'] = {
            'status_code': response.status_code, 
            'data': response.json()
        }
        return response

    def post(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        self.registry['post'] = {}
        self.registry['post'].update({'request': {
            'path': path, 
            'data': data,
            'format': format,
            'content_type': content_type,
        }})
        response = self.client.post(path, data=None, follow=False, **extra)
        self.registry['post'].update({'response': {
            'status_code': response.status_code, 
            'data': response.json()
        }})
        return response

    def put(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        self.registry['put'] = {}
        self.registry['put'].update({'request': {
            'path': path, 
            'data': data,
            'format': format,
            'content_type': content_type,
        }})
        response = self.client.put(path, data=None, follow=False, **extra)
        self.registry['put'].update({'response': {
            'status_code': response.status_code, 
            'data': response.json()
        }})
        return response

    def patch(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        self.registry['patch']['request'] = {
            'path': path, 
            'data': data,
            'format': format,
            'content_type': content_type,
        }
        response = self.client.get(path, data=None, follow=False, **extra)
        self.registry['patch']['response'] = {
            'status_code': response.status_code, 
            'data': response.json()
        }
        return response

    def delete(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        self.registry['delete']['request'] = {
            'path': path, 
            'data': data,
            'format': format,
            'content_type': content_type,
        }
        response = self.client.get(path, data=None, follow=False, **extra)
        self.registry['delete']['response'] = {
            'status_code': response.status_code, 
            'data': response.json()
        }
        return response

    def options(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        self.registry['options']['request'] = {
            'path': path, 
            'data': data,
            'format': format,
            'content_type': content_type,
        }
        response = self.client.get(path, data=None, follow=False, **extra)
        self.registry['options']['response'] = {
            'status_code': response.status_code, 
            'data': response.json()
        }
        return response

    def __getattr__(self, attr):
        if not attr in dir(self):
            return getattr(self.client, attr)
        return getattr(self, attr)


class BaseViewsetTest():
    """
    Класс для тестирования вьюсетов.
    """
    viewset = None
    obj_factory_class = None
    app_name = 'api_v1'
    url_basename = 'company-branches'
    save_requests = False
    requests_registry = {}      

    def get_client(self):
        if self.save_requests:
            return DocClient(self.requests_registry)
        return APIClient

    def get_action_url(self, action, *args, **kwargs):
        url = f'{self.app_name}:{self.url_basename}-{action}'
        return reverse(url, args=args, kwargs=kwargs)

    def setup_method(self, method):
        self.client = self.get_client()
        self.obj = self.obj_factory_class()
        self.post_data = generate_to_dict(self.obj_factory_class)
        self.patch_data = generate_to_dict(self.obj_factory_class)

    def teardown_class(cls):
        if cls.save_requests:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_name = f'{cls.viewset.__name__}.json'
            with open(os.path.join(dir_path, file_name), 'w') as fp:
                json.dump(cls.requests_registry, fp, ensure_ascii=False, indent=4)