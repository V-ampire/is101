from accounts.models import UserAccount

import factory


class AdminUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи администратора.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = UserAccount.ADMIN


class CompanyUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи юр. лица.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = UserAccount.COMPANY


class EmployeeUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи юр. лица.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = UserAccount.EMPLOYEE
