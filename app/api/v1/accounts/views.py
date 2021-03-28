from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from accounts.utils import get_users_uuid_without_profile
from accounts.models import Roles

from api.v1.accounts import serializers
from api.v1.accounts import mixins
from api.v1.permissions import IsOwnerOrAdmin, IsOwnerOrSuperuser, IsPermittedToEmployeeUser

from api.v1.mixins import ViewSetActionPermissionMixin


class CompanyAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin,
                        ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей юрлиц.
    Метод POST отключен, т.к. учетная запись создается одновременно с профилем.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    http_method_names = ['get', 'patch']
    permission_classes = [IsAdminUser]
    queryset = get_user_model().company_objects.all()
    serializer_class = serializers.CompanyUserAccountSerializer
    lookup_field = 'uuid'

    permission_action_classes = {
        "retrieve": [IsOwnerOrAdmin],
        "partial_update": [IsOwnerOrAdmin],
        "change-password": [IsOwnerOrAdmin],
    }


class EmployeeAccountsViewSet(mixins.ActiveControlViewMixin, mixins.ChangePasswordViewMixin,
                        ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей работников.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    Метод POST отключен, т.к. учетная запись создается одновременно с профилем.
    Метод DELETE отключен, т.к. учетная запись удаляется одновременно с профилем.
    """
    http_method_names = ['get', 'patch']
    permission_classes = [IsPermittedToEmployeeUser]
    queryset = get_user_model().employee_objects.all()
    serializer_class = serializers.EmployeeUserAccountSerializer
    lookup_field = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
    }


class AdminAccountViewSet(mixins.ChangePasswordViewMixin, viewsets.ModelViewSet):
    """
    Вьюсет для учетных записей администраторов.
    Доступны только действия для чтения, изменения и изменения пароля.
    """
    http_method_names = ['get', 'patch']
    permission_classes = [IsOwnerOrSuperuser]
    queryset = get_user_model().objects.filter(role=Roles.ADMIN)
    serializer_class = serializers.UserAccountSerializer
    lookup_field = 'uuid'

    def list(self, request):
        raise MethodNotAllowed('GET', detail='Список учетных записей недоступен.')


class UsersWithNoProfileView(generics.ListAPIView):
    """
    Список учетных записей юрлиц и работников у которых не заполнен профиль.
    """
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ReadOnlyUserAccountSerializer

    def get_queryset(self):
        users_uuid = get_users_uuid_without_profile()
        return get_user_model().objects.filter(uuid__in=users_uuid)


class UsersWithNoProfileCountView(APIView):
    """
    Количество учетных записей юрлиц и работников у которых не заполнен профиль.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users_uuid = get_users_uuid_without_profile()
        return Response({'count': len(users_uuid)})



