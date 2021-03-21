from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from companies import models, utils, validators

from api.v1.accounts.serializers import ReadOnlyUserAccountSerializer, CompanyUserAccountSerializer
from api.v1.branches.serializers import BranchListSerializer


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания юр. лица для админов.
    Содержит uuid учетной записи юрлица.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()

    class Meta:
        model = models.CompanyProfile
        fields = (
            'username',
            'password',
            'email',
            'title',
            'logo',
            'tagline',
            'inn',
            'ogrn',
            'city',
            'address',
            'phone',
        )

    def validate(self, data):
        user_serializer = CompanyUserAccountSerializer(data={
            'username': data['username'],
            'password': data['password'],
            'email': data['email']
        })
        user_serializer.is_valid(raise_exception=True)
        return data
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        return utils.create_company(username, email, password, **validated_data)


class CompanySerializerForAdmin(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для чтения юр. лица для админов.
    Содержит учетную запись.
    """
    user = ReadOnlyUserAccountSerializer()
    branches = BranchListSerializer(many=True)
    
    class Meta:
        model = models.CompanyProfile
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
            'phone',
            'url',
            'branches',
            'status',
        )
        read_only_fields = ('user', 'branches', 'status')
        extra_kwargs = {
            'url': {'view_name': 'api_v1:companies-detail', 'lookup_field': 'uuid'},
        }


class CompanySerializerForPermitted(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица для тех кому разрешен доступ.
    """
    branches = BranchListSerializer(many=True, read_only=True)

    class Meta:
        model = models.CompanyProfile
        fields = (
            'uuid',
            'title',
            'logo',
            'tagline',
            'inn',
            'ogrn',
            'city',
            'address',
            'phone',
            'branches'
        )


class CompanyListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для списка компаний.
    """
    class Meta:
        model = models.CompanyProfile
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