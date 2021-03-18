from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.positions.serializers import PositionSerializer
from api.v1.positions.validators import validate_status_param
from api.v1 import mixins
from api.v1.permissions import IsCompanyUser

from companies.models import Position
from companies import utils

from core.models import Statuses


class PositionViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для должностей.
    Для юрлиц доступнен только список активных должностей.
    """
    model_class = Position
    serializer_class = PositionSerializer
    lookup_field = 'uuid'
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    permission_action_classes = {
        "list": [IsAdminUser | IsCompanyUser],
    }

    def get_queryset(self):
        queryset = Position.objects.all()
        if not self.request.user.is_staff:
            return queryset.filter(status=Statuses.WORKS)
        filter_status = self.request.query_params.get('status', None)
        if filter_status:
            validate_status_param(filter_status)
            return queryset.filter(status=filter_status)
        return queryset

    @action(detail=True, methods=['patch'])
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу должности в архив.
        """
        position = self.get_object()
        utils.position_to_archive(position.uuid)
        return Response({'status': 'Должность переведена в архив.'})

    @action(detail=True, methods=['patch'])
    def to_work(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу должности в работу.
        """
        position = self.get_object()
        utils.position_to_work(position.uuid)
        return Response({'status': 'Должность в рабочем статусе.'})
        