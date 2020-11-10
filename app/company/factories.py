from company import models

from accounts import factories as accounts_factories

import factory
from faker import Faker


fake = Faker()



class CompanyFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели компании.
    """
    class Meta:
        model = models.Company

    user = factory.SubFactory(accounts_factories.CompanyUserAccountModelFactory)
    title = factory.Faker('company')
    inn = factory.Faker('pystr', max_chars=12)
    ogrn = factory.Faker('pystr', max_chars=15)
    city = factory.Faker('city')
    address = factory.Faker('address')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    logo = factory.django.ImageField(filename=fake.file_name(extension='jpg'))
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
    class Meta:
        model = models.Position

    title = factory.Faker('job')


class EmployeeFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели работника.
    """
    class Meta:
        model = models.Employee
        
    user = factory.SubFactory(accounts_factories.EmployeeUserAccountModelFactory)
    fio = factory.Faker('name')
    branch = factory.SubFactory(BranchFactory)
    position = factory.SubFactory(PositionFactory)
    date_of_birth = factory.Faker('date')
    pasport = factory.Faker('pystr')
    pasport_scan = factory.django.FileField(filename=fake.file_name(extension='pdf'))
