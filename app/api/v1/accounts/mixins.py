from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.accounts.serizlizers import ChangePasswordSerializer

from accounts.utils import change_password


class ChangePasswordViewMixin():
    """
    Миксин для вью с действием смены пароля.
    """
    @action(detail=True, methods=['post'])
    def change_password(self, request, uuid):
        user = get_object_or_404(get_user_model(), uuid=uuid)
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(user.pk, serializer.validated_data['password1'])
        return Response({'status': 'ok'})


class DeactivateViewMixin():
    """
    Миксин для вью с действием делающим учетную запись неактивной.
    """
    @action(detail=True)
    def deactivate(self, request, uuid):
        user = get_object_or_404(get_user_model(), uuid=uuid)
        user.deactivate()
        return Response({'status': 'ok'})




