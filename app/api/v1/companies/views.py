from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1.permissions import IsPermittedOrAdmin

from company.models import Company
from company.utils import delete_company


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, mixins.StatusViewSetMixin,
                        viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    Метод PUT отключен т.к. запрещено обновлять учетную запись через данный вьюсет.
    """
    model_class = Company
    queryset = Company.objects.all()
    lookup_field = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
        "retrieve": [IsPermittedOrAdmin],
        "create": [IsAdminUser],
        "update": [IsPermittedOrAdmin],
        "partial_update": [IsPermittedOrAdmin],
        "destroy": [IsAdminUser],
        "archivate": [IsAdminUser],
        "activate": [IsAdminUser],
    }

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.order_by('-status')

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.request.user.is_staff:
                return serializers.CompanyDetailSerializerForAdmin
            return serializers.CompanySerializerForPermitted

        if self.action == "list":
            return serializers.CompanyListSerializer

        if self.action == "create":
            return serializers.CompanyCreateSerializer
        
        if self.action == "partial_update":
            if self.request.user.is_staff:
                return serializers.CompanyDetailSerializerForAdmin
            return serializers.CompanySerializerForPermitted

    def perform_destroy(self, instance):
        delete_company(instance.pk)