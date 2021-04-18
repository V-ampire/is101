from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from api.v1 import mixins
from api.v1.employees import serializers
from api.v1.permissions import IsCompanyOwnerOrAdmin

from accounts.emails import get_email_fields
from accounts.tasks import send_account_created_message

from companies.models import EmployeeProfile
from companies import utils



class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работников.
    """
    model_class = EmployeeProfile
    lookup_field = 'uuid'
    company_uuid_kwarg = 'company_uuid'
    permission_classes = [IsCompanyOwnerOrAdmin]

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return EmployeeProfile.objects.filter(branch__uuid=self.kwargs['branch_uuid'])


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
        create_data = request.data.dict()
        create_data['branch'] = self.kwargs['branch_uuid']
        create_serializer = self.get_serializer(data=create_data)
        create_serializer.is_valid(raise_exception=True)
        employee = create_serializer.save()
        fields = get_email_fields(create_serializer, include=[
            'username',
            'password',
            'email',
            'fio',
            'date_of_birth',
            'pasport',
        ])
        send_account_created_message.delay(request.user.uuid, fields)
        context = self.get_serializer_context()
        employee_serializer = serializers.EmployeeSerializer(employee, context=context)
        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        utils.delete_employee(instance.uuid)

    @action(detail=True, methods=['patch'])
    def change_position(self, request, *args, **kwargs):
        """
        Изменение должности.
        """
        employee = self.get_object()
        change_data = request.data.dict()
        change_data['employee'] = employee.uuid
        change_serializer = serializers.ChangePositionSerializer(data=change_data)
        change_serializer.is_valid(raise_exception=True)
        changed_employee = utils.change_employee_position(
            change_serializer.validated_data.get('employee'),
            change_serializer.validated_data.get('position')
        )
        context = self.get_serializer_context()
        employee_serializer = serializers.EmployeeSerializer(changed_employee, context=context)
        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, headers=headers)

    @action(detail=True, methods=['patch'])
    def change_branch(self, request, *args, **kwargs):
        """
        Перевод в другой филиал.
        """
        employee = self.get_object()
        transfer_data = request.data.dict()
        transfer_data['employee'] = employee.uuid
        transfer_serializer = serializers.ChangeBranchSerializer(data=transfer_data)
        transfer_serializer.is_valid(raise_exception=True)
        transfered_employee = utils.transfer_employee_to_branch(
            transfer_serializer.validated_data.get('employee'),
            transfer_serializer.validated_data.get('branch')
        )
        context = self.get_serializer_context()
        employee_serializer = serializers.EmployeeSerializer(transfered_employee, context=context)
        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, headers=headers)

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


