from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import AnonymousUser

from api.v1 import permissions

from accounts.factories import CompanyUserAccountModelFactory

import pytest


@pytest.mark.django_db
class TestIsAdminOrOwnerCompanyUser():

    def setup_method(self, method):
        self.perm = permissions.IsAdminOrOwnerCompanyUser()
        self.rf = APIRequestFactory()

    def test_has_object_permission_with_admin_user(self, admin_user, company_user, mocker):
        view = mocker.Mock()
        request = self.rf.get('/')
        request.user = admin_user
        assert self.perm.has_object_permission(request, view, company_user)

    def test_has_object_permission_with_another_company_user(self, mocker):
        expected_user = CompanyUserAccountModelFactory()
        invalid_user = CompanyUserAccountModelFactory()
        view = mocker.Mock()
        request = self.rf.get('/')
        request.user = invalid_user
        assert not self.perm.has_object_permission(request, view, expected_user)

    def test_has_object_permission_with_own_company_user(self, company_user, mocker):
        view = mocker.Mock()
        request = self.rf.get('/')
        request.user = company_user
        assert self.perm.has_object_permission(request, view, company_user)

    def test_has_object_permission_with_employee_user(self, company_user, employee_user, mocker):
        view = mocker.Mock()
        request = self.rf.get('/')
        request.user = employee_user
        assert not self.perm.has_object_permission(request, view, company_user)

    def test_has_object_permission_with_anonymous_user(self, company_user, mocker):
        view = mocker.Mock()
        request = self.rf.get('/')
        request.user = AnonymousUser()
        assert not self.perm.has_object_permission(request, view, company_user)