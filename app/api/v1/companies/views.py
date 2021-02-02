from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1 import permissions

from companies.models import CompanyProfile
from companies import utils


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    Метод PUT отключен т.к. запрещено обновлять учетную запись через данный вьюсет.
    """
    model_class = CompanyProfile
    queryset = CompanyProfile.objects.all()
    lookup_field = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
        "retrieve": [permissions.IsPermittedToCompanyProfile],
        "create": [IsAdminUser],
        "partial_update": [permissions.IsPermittedToCompanyProfile],
        "destroy": [IsAdminUser],
        "to_archive": [IsAdminUser],
        "to_work": [IsAdminUser],
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
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу юрлица в архив.
        В качестве нагрузки может быть передан булевый параметр force
        {"force": True/False}, который определяет режим перевода в арихив связанных сущностей.
        """
        force = request.data.get('force', False)
        company = self.get_object()
        utils.company_to_archive(company.uuid, force=force)
        return Response({'status': 'Юрлицо переведено в архив. Учетная запись отключена.'})

    @action(detail=True, methods=['patch'])
    def to_work(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу юрлица в работу.
        """
        company = self.get_object()
        utils.company_to_work(company.uuid)
        return Response({'status': 'Юрлицо в рабочем статусе. Учетная запись активирована.'})