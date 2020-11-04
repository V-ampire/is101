from company import models

from accounts.facories import UserAccountModelFactory

import factory
from faker import Faker


fake = Faker()


class BusinessEntityFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели юридического лица.
    """
    class Meta:
        model = models.BusinessEntity

    title = factory.Faker('company')
    inn = factory.Faker('pystr', max_chars=12)
    inn = factory.Faker('pystr', max_chars=15)
    city = factory.Faker('city')
    address = factory.Faker('address')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')


class CompanyFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели компании.
    """
    class Meta:
        model = models.Company

    entity = factory.SubFactory(BusinessEntityFactory)
    title = factory.Faker('company')
    logo = factory.django.ImageField(filename=fake.file_path())
    tagline = factory.Faker('catch_phrase')


class BranchFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели филиала.
    """
    class Meta:
        model = models.Branch

    company = factory.SubFactory(CompanyFactory)
    city = factory.Faker('city')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')


class PositionFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели должности.
    """
    title = factory.Faker('job')


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели работника.
    """
    user = factory.SubFactory(UserAccountModelFactory)
    fio = factory.Faker('name')
    branch = factory.SubFactory(BranchFactory)
    position = factory.SubFactory(PositionFactory)
    date_of_birth = factory.Faker('date')
    pasport = factory.Faker('pystr')
    pasport_scan = factory.django.FileField(filename=fake.file_name())
