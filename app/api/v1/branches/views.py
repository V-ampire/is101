from rest_framework import viewsets

from api.v1 import mixins
from api.v1.permissions import IsPermittedOrAdmin
from api.v1.branches import serializers

from company.models import Branch


class BranchesViewSet(mixins.StatusViewSetMixin, viewsets.ModelViewSet):
    """
    Вьюсет для филиалов.
    """
    model_class = Branch
    queryset = Branch.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsPermittedOrAdmin]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.filter(company__uuid=self.kwargs['company_uuid'])

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BranchListSerializer
        return serializers.BranchSerializer