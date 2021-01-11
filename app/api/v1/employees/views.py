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

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EmployeeListSerizlizer
        return serializers.EmployeeSerializer