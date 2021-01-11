from django.utils.translation import gettext_lazy as _

from accounts import forms
from accounts.models import Roles, UserAccount

from faker import Faker
import pytest


fake = Faker()

@pytest.mark.django_db
def test_clean_is_superuser_for_company_role():
    tested_role = Roles.COMPANY
    tested_data = {
        'username': fake.user_name(),
        'is_superuser': True,
        'role': tested_role,
        'date_joined': fake.date()
    }
    form = forms.UserAccountChangeForm(data=tested_data)
    assert form.errors['__all__'] == [_(f'User with role {tested_role} can not be a superuser')]


@pytest.mark.django_db
def test_clean_is_superuser_for_employee_role():
    tested_role = Roles.EMPLOYEE
    tested_data = {
        'username': fake.user_name(),
        'is_superuser': True,
        'role': tested_role,
        'date_joined': fake.date()
    }
    form = forms.UserAccountChangeForm(data=tested_data)
    assert form.errors['__all__'] == [_(f'User with role {tested_role} can not be a superuser')]


@pytest.mark.django_db
def test_clean_is_superuser_for_admin_role():
    tested_role = Roles.ADMIN
    tested_data = {
        'username': fake.user_name(),
        'is_superuser': True,
        'role': tested_role,
        'date_joined': fake.date()
    }
    form = forms.UserAccountChangeForm(data=tested_data)
    assert not form.errors
    assert form.is_valid()