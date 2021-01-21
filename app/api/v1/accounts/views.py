from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

from api.v1.permissions import IsPermittedOrAdmin, IsCompanyOrAdmin
from api.v1.accounts import serializers
from api.v1.accounts import mixins

from api.v1.mixins import ViewSetActionPermissionMixin

from accounts.models import UserAccount


class CompanyAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей юрлиц.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUser]
    queryset = UserAccount.company_objects.all()
    serializer_class = serializers.CompanyUserAccountSerializer
    lookup_field = 'uuid'


class EmployeeAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin, 
                ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей работников.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUser]
    queryset = UserAccount.employee_objects.all()
    serializer_class = serializers.EmployeeUserAccountSerializer
    lookup_field = 'uuid'

    permission_action_classes = {
        'create': [IsCompanyOrAdmin],
        'partial_update': [IsPermittedOrAdmin],
        'activate': [IsPermittedOrAdmin],
        'deactivate': [IsPermittedOrAdmin],
        'change_password': [IsPermittedOrAdmin]
    }