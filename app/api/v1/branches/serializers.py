from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from api.v1.employees.serializers import EmployeeListSerizlizer

from companies.models import Branch, CompanyProfile
from companies.utils import create_branch


class BranchCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания филиала.
    """
    company = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = Branch
        fields = (
            'company',
            'uuid',
            'city',
            'address',
            'phone',
            'status'
        )

    def validate_company(self, company_uuid):
        if not CompanyProfile.objects.filter(uuid=company_uuid).exists():
            raise serializers.ValidationError(f'Юрлицо с uuid={company_uuid} не существует.')
        return company_uuid

    def create(self, validated_data):
        company_uuid = validated_data.pop('company')
        create_branch(company_uuid, **validated_data)



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