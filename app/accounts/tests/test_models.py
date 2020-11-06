from accounts.models import UserAccount
from accounts import facories 

import pytest

from faker import Faker


fake = Faker()


@pytest.mark.django_db
def test_is_staff():
    admin_user = UserAccount.objects.create_user(
        fake.user_name(), UserAccount.ADMIN, fake.password()
    )
    company_user = UserAccount.objects.create_user(
        fake.user_name(), UserAccount.COMPANY, fake.password()
    )
    employee_user = UserAccount.objects.create_user(
        fake.user_name(), UserAccount.EMPLOYEE, fake.password()
    )
    assert admin_user.is_staff == True
    assert company_user.is_staff == False
    assert employee_user.is_staff == False


@pytest.mark.django_db
def test_create_superuser():
    superuser = UserAccount.objects.create_superuser(fake.user_name(), fake.password())
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.role == UserAccount.ADMIN


@pytest.mark.django_db
def test_company_manager():
    admin_user = facories.AdminUserAccountModelFactory()
    company_user = facories.CompanyUserAccountModelFactory()
    employer_user = facories.EmployerUserAccountModelFactory()
    tested = UserAccount.company_objects.all()
    expected = UserAccount.objects.filter(role=UserAccount.COMPANY)
    assert set(tested) == set(expected)


@pytest.mark.django_db
def test_employer_manager():
    admin_user = facories.AdminUserAccountModelFactory()
    company_user = facories.CompanyUserAccountModelFactory()
    employee_user = facories.EmployeeUserAccountModelFactory()
    tested = UserAccount.employer_objects.all()
    expected = UserAccount.objects.filter(role=UserAccount.EMPLOYEE)
    assert set(tested) == set(expected)

