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
    password = serializers.CharField(write_only=True)
    position = serializers.UUIDField(format='hex_verbose', required=False)

    class Meta:
        model = EmployeeProfile
        fields = (
            'username',
            'password',
            'fio',
            'position',
            'date_of_birth',
            'pasport',
            'pasport_scan'
        )

    def validate(self, data):
        user_serializer = EmployeeUserAccountSerializer(data={
            'username': data['username'],
            'password': data['password']
        })
        user_serializer.is_valid(raise_exception=True)
        url_kwargs = self.context['view'].kwargs
        try:
            data['branch'] = url_kwargs['branch_uuid']
        except KeyError:
            raise NoReverseMatch('URL должен содержать UUID филиала.')
        return data

    def create(self, validated_data):
        branch_uuid = validated_data.pop('branch')
        position_uuid = validated_data.pop('position', None)
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        return utils.create_employee(username, password, branch_uuid, position_uuid=position_uuid, **validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели работника.
    """
    user = ReadOnlyUserAccountSerializer()
    company = serializers.ReadOnlyField()
    branch = serializers.StringRelatedField(read_only=True)
    position = serializers.StringRelatedField(read_only=True)

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
            'pasport_scan'
        )


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
            'position'
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-branch-employees-detail', 'lookup_field': 'uuid'},
        }
        

class ChangePositionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    class Meta:
        fields = ('uuid',)

    def validate_uuid(self, position_uuid):
        return validators.validate_position_for_change(position_uuid)


class ChangeBranchSerializer(serializers.Serializer):
    branch_uuid = serializers.UUIDField()
    employee_uuid = serializers.UUIDField()

    class Meta:
        fields = ('branch_uuid', 'employee_uuid')

    def validate(self, validated_data):
        branch_uuid = validated_data['branch_uuid']
        employee_uuid = validated_data['employee_uuid']
        validators.validate_branch_for_transfer(branch_uuid, employee_uuid)
        return validated_data
