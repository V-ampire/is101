from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


from company.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели работника.
    """
    company = serializers.ReadOnlyField()
    branch = serializers.StringRelatedField()
    position = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = (
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
