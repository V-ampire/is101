from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

from api.v1.accounts import serializers
from api.v1.accounts import mixins

from api.v1.mixins import ViewSetActionPermissionMixin


class CompanyAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей юрлиц.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdminUser]
    queryset = get_user_model().company_objects.all()
    serializer_class = serializers.CompanyUserAccountSerializer
    lookup_field = 'uuid'


class EmployeeAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей работников.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    Метод POST отключен, т.к. учетная запись создается одновременно с профилем.
    Метод DELETE отключен, т.к. учетная запись удаляется одновременно с профилем.
    """
    http_method_names = ['get', 'patch']
    permission_classes = [IsAdminUser]