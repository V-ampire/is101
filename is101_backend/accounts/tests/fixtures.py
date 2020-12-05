from accounts import factories

import pytest


@pytest.fixture
def admin_user(db):
    return factories.AdminUserAccountModelFactory()


@pytest.fixture
def company_user(db):
    return factories.CompanyUserAccountModelFactory()


@pytest.fixture
def employee_user(db):
    return factories.EmployeeUserAccountModelFactory()
