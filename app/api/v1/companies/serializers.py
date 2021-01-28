from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from companies import models, utils, validators

from api.v1.accounts.serializers import ReadOnlyUserAccountSerializer
from api.v1.branches.serializers import BranchListSerializer
from api.v1.companies import validators


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания юр. лица для админов.
    Содержит uuid учетной записи юрлица.
    """
    user = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = models.Company
        fields = (
            'user',
            'title',
            'logo',
            'tagline',
            'inn',
            'ogrn',
            'city',
            'address',
            'email',
            'phone',
        )

    def validate_user(self, user_uuid):
        """
        Возвращает объект accounts.UserAccount
        """
        try:
            user = get_user_model().company_objects.get(uuid=user_uuid)
        except get_user_model().DoesNotExists:
            raise serializers.ValidationError(f'Учетная запись юрлица с uuid={user_uuid} не существует.')
        validators.validate_company_user(user)
        return user.uuid
    
    def create(self, validated_data):
        user_uuid = validated_data.pop('user')
        return utils.create_company(user_uuid=user_uuid, **validated_data)


class CompanySerializerForAdmin(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для чтения юр. лица для админов.
    Содержит учетную запись.
    """
    user = ReadOnlyUserAccountSerializer()
    branches = BranchListSerializer(many=True)
    
    class Meta:
        model = models.Company
        fields = (
            'uuid',
            'user',
            'title',
            'logo',
            'tagline',
            'inn',
            'ogrn',
            'city',
            'address',
            'email',
            'phone',
            'url',
            'branches'
        )
        read_only_fields = ('user', 'branches')
        extra_kwargs = {
            'url': {'view_name': 'api_v1:companies-detail', 'lookup_field': 'uuid'},
        }


class CompanySerializerForPermitted(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица для тех кому разрешен доступ.
    """
    branches = BranchListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Company
        fields = (
            'title',
            'logo',
            'tagline',
            'inn',
            'ogrn',
            'city',
            'address',
            'email',
            'phone',
            'branches'
        )


class CompanyListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для списка компаний.
    """
    class Meta:
        model = models.Company
        fields = (
            'uuid',
            'url', 
            'city',
            'address',
            'title',
            'status'
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:companies-detail', 'lookup_field': 'uuid'},
        }