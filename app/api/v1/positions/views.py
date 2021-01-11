from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.positions.serializers import PositionSerializer
from api.v1.permissions import IsCompanyOrAdmin
from api.v1 import mixins

from company.models import Position


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
        "list": [IsCompanyOrAdmin],
    }

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(status=Position.ACTIVE)
        return self.queryset