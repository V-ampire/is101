from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.test import APIRequestFactory, force_authenticate

from api.v1.accounts import mixins

from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestChangePasswordMixin():
    
    def setup_method(self, method):
        class PasswordViewSet(mixins.ChangePasswordViewMixin, ModelViewSet):
            queryset = get_user_model().objects.all()
            lookup_field = 'uuid'
        self.view = PasswordViewSet.as_view({'patch': 'change_password'})
        self.factory = APIRequestFactory()

    def test_success_change_password(self, admin_user, company_user, mocker):
        mock_change = mocker.patch('api.v1.accounts.mixins.change_password')
        expected_password = fake.password()
        data = {
            'password1': expected_password,
            'password2': expected_password
        }
        url = f'/accounts/companies/{company_user.uuid}/change_password/'
        request_kwargs = {'uuid': company_user.uuid}
        request = self.factory.patch(url, data)
        force_authenticate(request, user=admin_user)
        response = self.view(request, **request_kwargs)

        mock_change.assert_called_with(company_user.pk, expected_password)


class TestActiveControlMixin():

    def setup_method(self, method):
        class ActiveControlViewSet(mixins.ActiveControlViewMixin, ModelViewSet):
            queryset = get_user_model().objects.all()
            lookup_field = 'uuid'
        self.activate_view = ActiveControlViewSet.as_view({'patch': 'activate'})
        self.deactivate_view = ActiveControlViewSet.as_view({'patch': 'deactivate'})
        self.factory = APIRequestFactory()

    def test_success_activate(self, admin_user, company_user, mocker):

        mock_activate = mocker.patch.object(company_user, 'activate')
        expected_password = fake.password()
        url = f'/accounts/companies/{company_user.uuid}/activate/'
        request_kwargs = {'uuid': company_user.uuid}
        request = self.factory.patch(url)
        force_authenticate(request, user=admin_user)
        response = self.activate_view(request, **request_kwargs)

        mock_activate.call_count == 1
    def test_success_deactivate(self, admin_user, company_user, mocker):

        mock_deactivate = mocker.patch.object(company_user, 'deactivate')
        expected_password = fake.password()
        url = f'/accounts/companies/{company_user.uuid}/change_password/'
        request_kwargs = {'uuid': company_user.uuid}
        request = self.factory.patch(url)
        force_authenticate(request, user=admin_user)
        response = self.deactivate_view(request, **request_kwargs)

        mock_deactivate.call_count == 1
