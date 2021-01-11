from rest_framework import serializers

from company.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели работника.
    """
    branch = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = (
            'uuid',
            'fio',
            'branch',
            'position',
            'date_of_birth',
            'pasport',
            'pasport_scan'
        )


class EmployeeListSerizlizer(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для списка сотрудников.
    """
    branch = serializers.StringRelatedField(read_only=True)
    position = serializers.StringRelatedField()

    parent_lookup_kwargs = {
		'branch_uuid': 'branch__uuid',
	}

    class Meta:
        model = Employee
        fields = (
            'uuid',
            'url',
            'fio',
            'branch',
            'position'
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:employee-detail', 'lookup_field': 'uuid'},
        }
