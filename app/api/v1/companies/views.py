from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1.permissions import IsOwnerOrAdmin

from company.models import Company
from company.utils import delete_company


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    Метод PUT отключен, т.к. изменение пароля происходит через отдельное действие.
    """
    model_class = Company
    queryset = Company.objects.all()
    lookup_field = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
        "retrieve": [IsOwnerOrAdmin],
        "create": [IsAdminUser],
        "update": [IsOwnerOrAdmin],
        "partial_update": [IsOwnerOrAdmin],
        "destroy": [IsAdminUser],
        "archivate": [IsAdminUser],
        "activate": [IsAdminUser],
    }

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner

        if self.action == "list":
            return serializers.CompanyListSerializer

        if self.action == "create":
            return serializers.CompanySerializerForAdmin

        if self.action == "update":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner
        
        if self.action == "partial_update":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner

    def perform_destroy(self, instance):
        delete_company(instance.pk)

    @action(detail=True)
    def archivate(self, request, *args, **kwargs):
        """
        Устанавливает объекту статус ARCHIVED.
        """
        obj = self.get_object()
        obj.status = self.model_class.ARCHIVED
        obj.save()
        return Response({'status': self.model_class.ARCHIVED})

    @action(detail=True)
    def activate(self, request, *args, **kwargs):
        """
        Устанавливает объекту статус ACTIVE.
        """
        obj = self.get_object()
        obj.status = self.model_class.ACTIVE
        obj.save()
        return Response({'status': self.model_class.ACTIVE})

