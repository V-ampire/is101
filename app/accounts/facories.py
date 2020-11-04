from django.contrib.auth import get_user_model

from accounts import models

import factory


class UserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи (пользователя).
    """
    class Meta:
        model = models.UserAccount

    username = factory.Faker('user_name')
    pasword = factory.Faker('password')
