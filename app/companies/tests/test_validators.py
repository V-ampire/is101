from django.core.exceptions import ValidationError, ObjectDoesNotExist

from accounts.factories import CompanyUserAccountModelFactory, EmployeeUserAccountModelFactory

from core.models import Statuses

from companies import validators
from companies import factories

from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestValidateCompanyToArchive():

    def setup_method(self, method):
        self.company = factories.CompanyProfileFactory.create()

    def test_with_no_company_branches(self):
        assert validators.validate_company_to_archive(self.company) is None

    def test_with_works_employees(self):
        branch = factories.BranchFactory.create(company=self.company)
        employee = factories.EmployeeProfileFactory.create(branch=branch, status=Statuses.WORKS)
        exp_message = f'Невозможно перевести юрлицо {self.company.title} в архив пока в нем числятся работающие сотрудники.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_company_to_archive(self.company)
        assert exc_info.value.message == exp_message
    
    def test_with_archived_employees(self):
        branch = factories.BranchFactory.create(company=self.company)
        employee = factories.EmployeeProfileFactory.create(branch=branch, status=Statuses.ARCHIVED)
        assert validators.validate_company_to_archive(self.company) is None

    def test_with_no_employees_in_branch(self):
        branch = factories.BranchFactory.create(company=self.company)
        assert validators.validate_company_to_archive(self.company) is None


@pytest.mark.django_db
class TestValidateBranchToArchive():

    def setup_method(self, method):
        self.branch = factories.BranchFactory.create()

    def test_with_no_employees(self):
        assert validators.validate_branch_to_archive(self.branch) is None

    def test_with_worked_employees(self):
        employee = factories.EmployeeProfileFactory.create(branch=self.branch, status=Statuses.WORKS)
        exp_message = f'Невозможно перевести филиал {self.branch} в архив пока в нем числятся работающие сотрудники.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_branch_to_archive(self.branch)
        assert exc_info.value.message == exp_message

    def test_with_archived_employees(self):
        employee = factories.EmployeeProfileFactory.create(branch=self.branch, status=Statuses.ARCHIVED)
        assert validators.validate_branch_to_archive(self.branch) is None


@pytest.mark.django_db
class TestValidateBranchToWork():

    def test_validate_with_archived_company(self):
        company = factories.CompanyProfileFactory(status=Statuses.ARCHIVED)
        branch = factories.BranchFactory.create(company=company, status=Statuses.ARCHIVED)
        exp_message = f'Невозможно перевести филиал {branch} в рабочий статус пока архивировано юрлицо {branch.company.title}.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_branch_to_work(branch)
        assert exc_info.value.message == exp_message

    def test_validate(self):
        company = factories.CompanyProfileFactory()
        branch = factories.BranchFactory.create(company=company, status=Statuses.ARCHIVED)
        assert validators.validate_branch_to_work(branch) is None


@pytest.mark.django_db
class TestValidateEmployeeToWork():

    def test_with_archived_branch(self):
        branch = factories.BranchFactory(status=Statuses.ARCHIVED)
        employee = factories.EmployeeProfileFactory.create(branch=branch, status=Statuses.ARCHIVED)
        exp_message = f'Невозможно перевести работника {employee.fio} в рабочий статус '\
                    + f'пока архивирован филиал {employee.branch} '\
                    + f'или юрлицо {employee.branch.company.title}.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_employee_to_work(employee)
        assert exc_info.value.message == exp_message

    def test_with_archived_company(self):
        company = factories.CompanyProfileFactory(status=Statuses.ARCHIVED)
        branch = factories.BranchFactory(company=company)
        employee = factories.EmployeeProfileFactory.create(branch=branch, status=Statuses.ARCHIVED)
        exp_message = f'Невозможно перевести работника {employee.fio} в рабочий статус '\
                    + f'пока архивирован филиал {employee.branch} '\
                    + f'или юрлицо {employee.branch.company.title}.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_employee_to_work(employee)
        assert exc_info.value.message == exp_message

    def test_validate(self):
        employee = factories.EmployeeProfileFactory.create(status=Statuses.ARCHIVED)


@pytest.mark.django_db
class TestValidateBranchForTransfer():

    def setup_method(self, method):
        self.employee = factories.EmployeeProfileFactory()

    def test_validate_branch_in_archive(self):
        branch = factories.BranchFactory(status=Statuses.ARCHIVED)
        exp_message = f'Невозможно перевести работника - филиал {branch} в архиве.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_branch_for_transfer(branch, self.employee)
        assert exc_info.value.message == exp_message

    def test_validate_with_different_companies(self):
        branch = factories.BranchFactory()
        exp_message = f'Невозможно перевести работника в филиал другого юрлица.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_branch_for_transfer(branch, self.employee)
        assert exc_info.value.message == exp_message

    def test_validate(self):
        branch = factories.BranchFactory(company=self.employee.branch.company)
        assert validators.validate_branch_for_transfer(branch, self.employee) is None


@pytest.mark.django_db
class TestPositionForChange():
    
    def test_validate_with_archived(self):
        position = factories.PositionFactory(status=Statuses.ARCHIVED)
        exp_message = f'Должность {position.title} находится в архиве.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_position_for_change(position)
        assert exc_info.value.message == exp_message

    def test_validate(self):
        position = factories.PositionFactory()
        assert validators.validate_position_for_change(position) is None


@pytest.mark.django_db
class TestValidateCompanyUser():

    def test_call_is_company_user(self, mocker):
        mock_is_user = mocker.patch('companies.validators.is_company_user')
        tested_user = CompanyUserAccountModelFactory.create()
        validators.validate_company_user(tested_user)
        mock_is_user.assert_called_with(tested_user)

    def test_validate_with_user_with_profile(self):
        profile = factories.CompanyProfileFactory.create()
        tested_user = profile.user
        exp_message = f"К учетной записи {tested_user.username} уже привязан профиль юрлица."
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_company_user(tested_user)
        assert exc_info.value.message == exp_message

    def test_validate_with_invalid_user_role(self):
        tested_user = EmployeeUserAccountModelFactory.create()
        exp_message = f"Учетная запись {tested_user.username} не может быть использована для профиля юрлица"
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_company_user(tested_user)
        assert exc_info.value.message == exp_message

    def test_success_validate(self):
        tested_user = CompanyUserAccountModelFactory.create()
        assert validators.validate_company_user(tested_user) is None



@pytest.mark.django_db
class TestValidateEmployeeUser():

    def test_call_is_cemployee_user(self, mocker):
        mock_is_user = mocker.patch('companies.validators.is_employee_user')
        tested_user = EmployeeUserAccountModelFactory.create()
        validators.validate_employee_user(tested_user)
        mock_is_user.assert_called_with(tested_user)

    def test_validate_with_user_with_profile(self):
        profile = factories.EmployeeProfileFactory.create()
        tested_user = profile.user
        exp_message = f"К учетной записи {tested_user.username} уже привязан профиль работника."
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_employee_user(tested_user)
        assert exc_info.value.message == exp_message

    def test_validate_with_invalid_user_role(self):
        tested_user = CompanyUserAccountModelFactory.create()
        exp_message = f"Учетная запись {tested_user.username} не может быть использована для профиля работника"
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            validators.validate_employee_user(tested_user)
        assert exc_info.value.message == exp_message

    def test_success_validate(self):
        tested_user = EmployeeUserAccountModelFactory.create()
        assert validators.validate_employee_user(tested_user) is None