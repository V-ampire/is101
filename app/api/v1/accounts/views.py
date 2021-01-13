from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

from api.v1.permissions import IsPermittedOrAdmin
from api.v1.accounts import serizlizers
from api.v1.accounts import mixins

from accounts.models import UserAccount


class CompanyAccountsViewSet(mixins.DeactivateViewMixin, mixins.ChangePasswordViewMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей юрлиц.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    hhttp_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUser]
    queryset = UserAccount.company_objects.all()
    serializer_class = serizlizers.CompanyUserAccountSerializer
    lookup_field = 'uuid'


class EmployeeAccountsViewSet(mixins.DeactivateViewMixin, mixins.ChangePasswordViewMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей работников.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    hhttp_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsPermittedOrAdmin]
    queryset = UserAccount.employee_objects.all()
    serializer_class = serizlizers.EmployeeUserAccountSerializer
    lookup_field = 'uuid'