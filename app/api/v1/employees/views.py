from rest_framework import viewsets

from api.v1 import mixins
from api.v1.permissions import IsPermittedOrAdmin
from api.v1.employees import serializers

from company.models import Employee


class EmployeeViewSet(mixins.StatusViewSetMixin, viewsets.ModelViewSet):
    """
    Вьюсет для филиалов.
    """
    model_class = Employee
    queryset = Employee.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsPermittedOrAdmin]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EmployeeListSerizlizer
        return serializers.EmployeeSerializer

    def get_queryset(self):
        return self.queryset.filter(branch__uuid=self.kwargs['branch_uuid'])