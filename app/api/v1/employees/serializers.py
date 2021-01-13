from rest_framework import serializers

from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.v1.accounts.serizlizers import ReadOnlyUserAccountSerializer

from api.v1.positions.serializers import PositionSerializer

from api.v1.employees.validators import validate_position_for_change, validate_branch_for_transfer

from company.models import Employee, Position, Branch


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели работника.
    """
    user = ReadOnlyUserAccountSerializer()
    company = serializers.ReadOnlyField()
    branch = serializers.StringRelatedField(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
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


class ChangePositionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    class Meta:
        fields = ('uuid',)

    def validate_uuid(self, position_uuid):
        return validate_position_for_change(position_uuid)


class ChangeBranchSerializer(serializers.Serializer):
    branch_uuid = serializers.UUIDField()
    employee_uuid = serializers.UUIDField()

    class Meta:
        fields = ('branch_uuid', 'employee_uuid')

    def validate(self, validated_data):
        branch_uuid = validated_data['branch_uuid']
        employee_uuid = validated_data['employee_uuid']
        validate_branch_for_transfer(branch_uuid, employee_uuid)
        return validated_data


class EmployeeListSerizlizer(NestedHyperlinkedModelSerializer):
    """
    Сериалайзер для списка сотрудников.
    """
    position = serializers.StringRelatedField()

    parent_lookup_kwargs = {
        'company_uuid': 'branch__company__uuid',
		'branch_uuid': 'branch__uuid',
	}

    class Meta:
        model = Employee
        fields = (
            'uuid',
            'url',
            'fio',
            'position'
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-branch-employees-detail', 'lookup_field': 'uuid'},
        }

