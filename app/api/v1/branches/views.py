from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

from api.v1 import mixins
from api.v1.validators import validate_status_param
from api.v1.permissions import IsCompanyOwnerOrAdmin
from api.v1.branches import serializers

from companies.models import Branch
from companies import utils


class BranchesViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для филиалов.
    """
    model_class = Branch
    lookup_field = 'uuid'
    company_uuid_kwarg = 'company_uuid'
    permission_classes = [IsCompanyOwnerOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    permission_action_classes = {
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        queryset = Branch.objects.filter(company__uuid=self.kwargs[self.company_uuid_kwarg])
        filter_status = self.request.query_params.get('status', None)
        if filter_status:
            validate_status_param(filter_status)
            return queryset.filter(status=filter_status)
        return queryset


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BranchListSerializer
        elif self.action == 'create':
            return serializers.BranchCreateSerializer
        return serializers.BranchSerializer

    def perform_destroy(self, instance):
        utils.delete_branch(instance.uuid)

    def create(self, request, *args, **kwargs):
        create_data = request.data.dict()
        create_data['company_uuid'] = self.kwargs[self.company_uuid_kwarg]
        create_serializer = self.get_serializer(data=create_data)
        create_serializer.is_valid(raise_exception=True)
        branch = create_serializer.save()
        context = self.get_serializer_context()
        branch_serializer = serializers.BranchSerializer(branch, context=context)
        headers = self.get_success_headers(branch_serializer.data)
        return Response(branch_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'])
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу филиала в архив.
        В качестве нагрузки может быть передан булевый параметр force
        {"force": True/False}, который определяет режим перевода в арихив связанных сущностей.
        """
        if request.data and request.content_type != 'application/json':
            raise ParseError(detail='Данные должны быть переданы в формате application/json.')
        force = request.data.get('force', False)
        branch = self.get_object()
        utils.branch_to_archive(branch.uuid, force=force)
        return Response({'status': 'Филиал переведен в архив.'})

    @action(detail=True, methods=['patch'])
    def to_work(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу филиала в работу.
        """
        branch = self.get_object()
        utils.branch_to_work(branch.uuid)
        return Response({'status': 'Филиал в рабочем статусе.'})
    