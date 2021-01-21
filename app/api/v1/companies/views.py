from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1.permissions import IsPermittedOrAdmin

from company.models import Company
from company import utils


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
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
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForPermitted

        if self.action == "list":
            return serializers.CompanyListSerializer

        if self.action == "create":
            return serializers.CompanyCreateSerializer
        
        if self.action == "partial_update":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForPermitted

    def perform_destroy(self, instance):
        utils.delete_company(instance.uuid)

    @action(detail=True, methods=['patch'])
    def archivate(self, request, *args, **kwargs):
        """
        Устанавливает юрлицу архиный статус и отключает учетку.
        """
        company = self.get_object()
        utils.archivate_company(company.uuid)
        return Response({'status': 'Юрлицо переведено в архив. Учетная запись отключена.'})

    @action(detail=True, methods=['patch'])
    def activate(self, request, *args, **kwargs):
        """
        Устанавливает объекту статус ACTIVE.
        Метод GET.
        """
        company = self.get_object()
        utils.activate_company(company.uuid)
        return Response({'status': 'Юрлицо активно. Учетная запись активирована.'})