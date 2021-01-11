from django.utils import timezone

from accounts.models import UserAccount, IPAddress, Roles

import factory


class BlockedIPAddressFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для моделей заблокированных IP.
    """
    class Meta:
        model = IPAddress
    
    ip = factory.Faker('ipv4')
    unblock_time = factory.Faker('date_time_this_month', before_now=False, after_now=True,
                                    tzinfo=timezone.get_current_timezone())
    is_blocked = True


class NotBlockedIPAddressFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для моделей заблокированных IP.
    """
    class Meta:
        model = IPAddress
    
    ip = factory.Faker('ipv4')
    unblock_time = None
    is_blocked = False


class AdminUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи администратора.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = Roles.ADMIN


class CompanyUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи юр. лица.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = Roles.COMPANY


class EmployeeUserAccountModelFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели учетной записи юр. лица.
    """
    class Meta:
        model = UserAccount

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    role = Roles.EMPLOYEE
