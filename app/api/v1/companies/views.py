from rest_framework.exceptions import ParseError
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1.permissions import IsCompanyOwnerOrAdmin

from companies.models import CompanyProfile
from companies import utils


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    Метод PUT отключен т.к. запрещено обновлять учетную запись через данный вьюсет.
    """
    model_class = CompanyProfile
    lookup_field = 'uuid'
    company_uuid_kwarg = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
        "retrieve": [IsCompanyOwnerOrAdmin],
        "create": [IsAdminUser],
        "partial_update": [IsCompanyOwnerOrAdmin],
        "destroy": [IsAdminUser],
        "to_archive": [IsAdminUser],
        "to_work": [IsAdminUser],
    }

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CompanyProfile.objects.all().order_by('-status')

    def get_serializer_class(self):

        if self.action == "list":
            return serializers.CompanyListSerializer

        elif self.action == "create":
            return serializers.CompanyCreateSerializer

        else:
            return serializers.CompanyDetailSerializer
        
    def create(self, request, *args, **kwargs):
        """
        Создать учетную запись.
        Создать профиль.
        """
        create_serializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        company = create_serializer.save()
        context = self.get_serializer_context()
        company_serializer = serializers.CompanySerializerForAdmin(company, context=context)
        headers = self.get_success_headers(company_serializer.data)
        return Response(company_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_destroy(self, instance):
        utils.delete_company(instance.uuid)

    @action(detail=True, methods=['patch'])
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу юрлица в архив.
        В качестве нагрузки может быть передан булевый параметр force
        {"force": True/False}, который определяет режим перевода в арихив связанных сущностей.
        """
        if request.data and request.content_type != 'application/json':
            raise ParseError(detail='Данные должны быть переданы в формате application/json.')
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