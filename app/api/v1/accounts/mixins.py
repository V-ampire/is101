from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.accounts.serializers import ChangePasswordSerializer

from accounts.utils import change_password, is_employee_user
from accounts.models import Roles


class ChangePasswordViewMixin():
    """
    Миксин для вью с действием смены пароля.
    """
    @action(detail=True, methods=['patch'])
    def change_password(self, request, uuid):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(user.pk, serializer.validated_data['password1'])
        return Response({'status': 'Пароль изменен.'})


class ActiveControlViewMixin():
    """
    Миксин для вью с действием делающим учетную запись активной/неактивной.
    """
    @action(detail=True, methods=['patch'])
    def deactivate(self, request, uuid):
        user = self.get_object()
        user.deactivate()
        return Response({'status': 'Пользователь в неактивном статусе.'})

    @action(detail=True, methods=['patch'])
    def activate(self, request, uuid):
        user = self.get_object()
        user.activate()
        return Response({'status': 'Пользователь в активном статусе.'})

