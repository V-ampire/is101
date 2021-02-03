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
    queryset = Branch.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsPermittedToBranch]

    permission_action_classes = {
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return self.queryset.filter(company__uuid=self.kwargs['company_uuid'])

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BranchListSerializer
        return serializers.BranchSerializer

    def perform_destroy(self, instance):
        utils.delete_branch(instance.uuid)

    @action(detail=True, methods=['patch'])
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу филиала в архив.
        В качестве нагрузки может быть передан булевый параметр force
        {"force": True/False}, который определяет режим перевода в арихив связанных сущностей.
        """
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
    