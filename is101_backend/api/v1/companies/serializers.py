from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from company import models


class CompanyUserAccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для учетной записи юр. лица.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        return get_user_model().company_objects.create_account(username, password)

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class CompanySerializerForAdmin(serializers.HyperlinkedModelSerializer):
    """
    Сериалайзер для юр. лица для админов.
    """
    user = CompanyUserAccountSerializer()
    
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
            'url'
        )
        extra_kwargs = {
            'url': {'view_name': 'api_v1:company-detail', 'lookup_field': 'uuid'},
        }

    def validate_user(self, user_data):
        """
        Если вызывается обновление учетной записи, то выдаем ошибку
        т.к. чтобы обновить пароль необходимо использовать действие сброса пароля.
        """
        if self.instance and user_data.get('password', None):
            raise serializers.ValidationError(
                "Для изменения пароля используйте функцию сброса пароля"
            )
        return user_data


    def create(self, validated_data):
        """
        1. Создать учетную запись
        2. Создать юр.лицо
        """
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = get_user_model().company_objects.create_account(**user_data)
            return models.Company.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """
        1. Если обновляется username - обновить учетную запись.
        2. Обновить юрлицо.
        """
        with transaction.atomic():
            user_data = validated_data.pop('user', None)
            if user_data:
                user = get_user_model().company_objects.get(pk=instance.user.pk)
                username = user_data['username']
                get_user_model().company_objects.filter(pk=instance.user.pk).update(
                    username=username)
            return super().update(instance, validated_data)


class CompanySerializerForOwner(serializers.ModelSerializer):
    """
    Сериалайзер для юр. лица для владельца юрлица.
    Юр. лицо не может менять свою учетную запись.
    """

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
            'url': {'view_name': 'api_v1:company-detail', 'lookup_field': 'uuid'},
        }
