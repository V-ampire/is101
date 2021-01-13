from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.v1.employees.serializers import EmployeeListSerizlizer

from company.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    """
    Сериалайзер филиала.
    """
    company = serializers.StringRelatedField(read_only=True)
    employees = EmployeeListSerizlizer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = (
            'company',
            'uuid',
            'city',
            'address',
            'phone',
            'employees',
            'status'
        )


class BranchListSerializer(NestedHyperlinkedModelSerializer):
    """
    Сериалайзер для списка филиалов.
    """
    parent_lookup_kwargs = {
		'company_uuid': 'company__uuid',
	}
    class Meta:
        model = Branch
        fields = (
            'uuid',
            'url',
            'city',
            'address',
            'phone',
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-branches-detail', 'lookup_field': 'uuid'},
        }