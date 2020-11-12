from django.contrib.auth import get_user_model

from rest_framework import serializers

from company import models as company_models


class CompanyUserAccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учетной записи юр. лица.
    """
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class CompanySerializerForAdmin(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица для админов.
    """
    user = CompanyUserAccountSerializer()
    
    class Meta:
        model = company_models.Company
        fields = '__all__'


class CompanySerializerForOwner(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица для владельца юрлица.
    """
    username = serializers.SerializerMethodField()

    class Meta:
        model = company_models.Company
        fields = (
            'username',
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
    
    def get_username(self, obj):
        return obj.user.username


class CompanyListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для списка компаний.
    """
    class Meta:
        model = company_models.Company
        fields = ('url', 'city', 'title', 'status')
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-detail', 'lookup_field': 'uuid'},
        }
