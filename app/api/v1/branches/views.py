from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1 import mixins
from api.v1.permissions import IsPermittedToBranch
from api.v1.branches import serializers

from companies.models import Branch


class BranchesViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для филиалов.
    """
    model_class = Branch
    lookup_field = 'uuid'
    permission_classes = [IsPermittedToBranch]
    http_method_names = ['get', 'post', 'patch', 'delete']

    permission_action_classes = {
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return Branch.objects.filter(company__uuid=self.kwargs['company_uuid'])

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BranchListSerializer
        elif self.action == 'create':
            return serializers.BranchCreateSerializer
        return serializers.BranchSerializer

    def perform_destroy(self, instance):
        utils.delete_branch(instance.uuid)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        create_data = request.data
        create_data['company'] = self.kwargs['company_uuid']
        create_serializer = serializer_class(data=create_data)
        create_serializer.is_valid(raise_exception=True)
        branch = create_serializer.save()
        branch_serializer = serializers.BranchSerializer(branch)
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
        utils.branch_to_work(company.uuid)
        return Response({'status': 'Филиал в рабочем статусе.'})
    