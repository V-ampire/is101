from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response


from api.v1 import mixins
from api.v1.employees import serializers
from api.v1.permissions import IsPermittedToEmployeeProfile

from companies.models import EmployeeProfile
from companies.utils import change_employee_position, transfer_employee_to_branch


class EmployeeViewSet(mixins.StatusViewSetMixin, viewsets.ModelViewSet):
    """
    Вьюсет для работников.
    """
    model_class = Employee
    queryset = Employee.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsPermittedToEmployeeProfile]

    http_method_names = ['get', 'post', 'patch', 'delete']

#     @action(detail=True, methods=['post'])
#     def change_position(self, request, *args, **kwargs):
#         """
#         Изменение должности.
#         """
#         serializer = serializers.ChangePositionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         employee_uuid = kwargs.get('uuid')
#         new_position_uuid = serializer.validated_data.get('uuid')
#         employee = change_employee_position(employee_uuid, new_position_uuid)
#         # FIXME Исключение если не существуют
#         employee_serizlizer = serializers.EmployeeSerializer(employee)
#         return Response(employee_serizlizer.data)

#     @action(detail=True, methods=['post'])
#     def change_branch(self, request, *args, **kwargs):
#         """
#         Перевод в другой филиал.
#         """
#         serializer = serializers.ChangeBranchSerializer(data={
#             'employee_uuid': kwargs.get('uuid'),
#             'branch_uuid': request.data.get('uuid')
#         })
#         serializer.is_valid(raise_exception=True)
#         employee_uuid = serializer.validated_data.get['employee_uuid']
#         branch_uuid = serializer.validated_data.get['branch_uuid']
#         employee = transfer_employee_to_branch(employee_uuid, branch_uuid)
#         employee_serizlizer = serializers.EmployeeSerializer(employee)
#         return Response(employee_serizlizer.data)

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return serializers.EmployeeListSerizlizer
#         return serializers.EmployeeSerializer

#     def get_queryset(self):
#         return self.queryset.filter(branch__uuid=self.kwargs['branch_uuid'])
