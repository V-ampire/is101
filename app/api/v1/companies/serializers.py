from django.contrib.auth import get_user_model

from rest_framework import serializers

from company import models as company_models


class CompanyAccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учетной записи юр. лица.
    """
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица.
    """
    class Meta:
        model = company_models.Company
        fields = '__all__'


class CompanyListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для списка компаний.
    """
    class Meta:
        model = company_models.Company
        fields = ('city', 'title', 'status')