from accounts.models import UserAccount, Roles
from accounts import factories

from companies.factories import EmployeeProfileFactory

import pytest

from faker import Faker


fake = Faker()


@pytest.mark.django_db
def test_is_staff():
    admin_user = UserAccount.objects.create_user(
        fake.user_name(), fake.email(), Roles.ADMIN, fake.password()
    )
    company_user = UserAccount.objects.create_user(
        fake.user_name(), fake.email(), Roles.COMPANY, fake.password()
    )
    employee_user = UserAccount.objects.create_user(
        fake.user_name(), fake.email(), Roles.EMPLOYEE, fake.password()
    )
    assert admin_user.is_staff == True
    assert company_user.is_staff == False
    assert employee_user.is_staff == False


@pytest.mark.django_db
def test_create_superuser():
    superuser = UserAccount.objects.create_superuser(fake.user_name(), fake.email(), fake.password())
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.role == Roles.ADMIN


@pytest.mark.django_db
def test_company_manager():
    admin_user = factories.AdminUserAccountModelFactory()
    company_user = factories.CompanyUserAccountModelFactory()
    employer_user = factories.EmployeeUserAccountModelFactory()
    tested = UserAccount.company_objects.all()
    expected = UserAccount.objects.filter(role=Roles.COMPANY)
    assert set(tested) == set(expected)


@pytest.mark.django_db
def test_employee_manager():
    admin_user = factories.AdminUserAccountModelFactory()
    company_user = factories.CompanyUserAccountModelFactory()
    employee_user = factories.EmployeeUserAccountModelFactory()
    tested = UserAccount.employee_objects.all()
    expected = UserAccount.objects.filter(role=Roles.EMPLOYEE)
    assert set(tested) == set(expected)

