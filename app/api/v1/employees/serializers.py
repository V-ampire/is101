from django.urls import NoReverseMatch

from rest_framework import serializers

from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.v1.accounts.serializers import ReadOnlyUserAccountSerializer, EmployeeUserAccountSerializer

from api.v1.positions.serializers import PositionSerializer

from companies.models import EmployeeProfile, Position, Branch
from companies import validators
from companies import utils


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для валидации данных для создания работника.
    """
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    branch = serializers.UUIDField(format='hex_verbose')
    position = serializers.UUIDField(format='hex_verbose', required=False)

    class Meta:
        model = EmployeeProfile
        fields = (
            'username',
            'password',
            'email',
            'branch',
            'fio',
            'position',
            'date_of_birth',
            'pasport',
            'pasport_scan',
        )

    def validate(self, data):
        user_serializer = EmployeeUserAccountSerializer(data={
            'username': data['username'],
            'password': data['password'],
            'email': data['email']
        })
        user_serializer.is_valid(raise_exception=True)
        return data

    def create(self, validated_data):
        branch_uuid = validated_data.pop('branch')
        position_uuid = validated_data.pop('position', None)
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        return utils.create_employee(username, email, password, branch_uuid, position_uuid=position_uuid, **validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели работника.
    """
    user = ReadOnlyUserAccountSerializer()
    company = serializers.ReadOnlyField()
    branch = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = EmployeeProfile
        fields = (
            'user',
            'uuid',
            'fio',
            'company',
            'branch',
            'position',
            'date_of_birth',
            'pasport',
            'pasport_scan',
            'status',
        )
        read_only_fields = ('user', 'company', 'branch', 'position', 'status')


class EmployeeListSerizlizer(NestedHyperlinkedModelSerializer):
    """
    Сериалайзер для списка сотрудников.
    """
    position = serializers.StringRelatedField(read_only=True)

    parent_lookup_kwargs = {
        'company_uuid': 'branch__company__uuid',
		'branch_uuid': 'branch__uuid',
	}

    class Meta:
        model = EmployeeProfile
        fields = (
            'uuid',
            'url',
            'fio',
            'position',
            'status',
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-branch-employees-detail', 'lookup_field': 'uuid'},
        }
        

class ChangePositionSerializer(serializers.Serializer):
    position = serializers.UUIDField()
    employee = serializers.UUIDField()

    class Meta:
        fields = ('position', 'employee')

    def validate_position(self, position_uuid):
        try:
            position = Position.objects.get(uuid=position_uuid)
        except Position.DoesNotExist:
            raise serializers.ValidationError(f'Должность с uuid={position_uuid} не существует.')
        validators.validate_position_for_change(position)
        return position_uuid


class ChangeBranchSerializer(serializers.Serializer):
    branch = serializers.UUIDField()
    employee = serializers.UUIDField()

    class Meta:
        fields = ('branch', 'employee')

    def validate(self, validated_data):
        branch_uuid = validated_data['branch']
        employee_uuid = validated_data['employee']
        try:
            branch = Branch.objects.get(uuid=branch_uuid)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(f'Филиал с uuid={branch_uuid} не существует.')
        
        try:
            employee = EmployeeProfile.objects.get(uuid=employee_uuid)
        except EmployeeProfile.DoesNotExist:
            raise serializers.ValidationError(f'Работник с uuid={employee_uuid} не существует.')
        validators.validate_branch_for_transfer(branch, employee)
        return validated_data
