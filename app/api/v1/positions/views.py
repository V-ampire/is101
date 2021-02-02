from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.positions.serializers import PositionSerializer
from api.v1 import mixins
from api.v1.permissions import IsCompanyUser

from companies.models import Position

from core.models import Statuses


class PositionViewSet(mixins.ViewSetActionPermissionMixin, mixins.StatusViewSetMixin, 
                        viewsets.ModelViewSet):
    """
    Вьюсет для должностей.
    Для юрлиц доступнен только список активных должностей.
    """
    model_class = Position
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    lookup_field = 'uuid'
    permission_classes = [IsAdminUser]

    permission_action_classes = {
        "list": [IsAdminUser | IsCompanyUser],
    }

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(status=Statuses.WORKS)
        return self.queryset
        