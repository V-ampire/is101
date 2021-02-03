from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from api.v1 import mixins
from api.v1.employees import serializers
from api.v1.permissions import IsPermittedToEmployeeProfile

from companies.models import EmployeeProfile
from companies.utils import change_employee_position, transfer_employee_to_branch


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работников.
    """
    model_class = EmployeeProfile
    queryset = EmployeeProfile.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsPermittedToEmployeeProfile]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.filter(branch__uuid=self.kwargs['branch_uuid'])


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EmployeeListSerizlizer
        elif self.action == 'create':
            return serializers.EmployeeCreateSerializer
        else:
            return serializers.EmployeeSerializer

    def create(self, request, *args, **kwargs):
        """
        Создать учетную запись.
        Создать профиль.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        import pdb; pdb.set_trace()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        utils.delete_employee(instance.uuid)

    @action(detail=True, methods=['patch'])
    def change_position(self, request, *args, **kwargs):
        """
        Изменение должности.
        """
        serializer = serializers.ChangePositionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee_uuid = kwargs.get('uuid')
        new_position_uuid = serializer.validated_data.get('uuid')
        employee = change_employee_position(employee_uuid, new_position_uuid)
        # FIXME Исключение если не существуют
        employee_serializer = serializers.EmployeeSerializer(employee)
        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, headers=headers)

    @action(detail=True, methods=['patch'])
    def change_branch(self, request, *args, **kwargs):
        """
        Перевод в другой филиал.
        """
        serializer = serializers.ChangeBranchSerializer(data={
            'employee_uuid': kwargs.get('uuid'),
            'branch_uuid': request.data.get('uuid')
        })
        serializer.is_valid(raise_exception=True)
        employee_uuid = serializer.validated_data.get['employee_uuid']
        branch_uuid = serializer.validated_data.get['branch_uuid']
        employee = transfer_employee_to_branch(employee_uuid, branch_uuid)
        employee_serializer = serializers.EmployeeSerializer(employee)
        return Response(employee_serializer.data)

    @action(detail=True, methods=['patch'])
    def to_archive(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу работника в архив.
        """
        employee = self.get_object()
        utils.employee_to_archive(employee.uuid)
        return Response({'status': 'Работник переведен в архив. Учетная запись отключена.'})

    @action(detail=True, methods=['patch'])
    def to_work(self, request, *args, **kwargs):
        """
        Выполняет действия по переводу работника в работу.
        """
        employee = self.get_object()
        utils.employee_to_work(employee.uuid)
        return Response({'status': 'Работник в рабочем статусе. Учетная запись активирована.'})

