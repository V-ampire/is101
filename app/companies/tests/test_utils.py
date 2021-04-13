from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from accounts.factories import CompanyUserAccountModelFactory

from companies import factories
from companies.models import CompanyProfile, EmployeeProfile, Branch
from companies import utils

from core.models import Statuses

from factory_generator import generate_to_dict, generate_to_db
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCreateCompany():

    def test_create(self, admin_user):
        user = generate_to_dict(CompanyUserAccountModelFactory)
        create_data = generate_to_dict(factories.CompanyProfileFactory)
        create_data.pop('user')
        tested_company = utils.create_company(
            admin_user,
            user['username'], 
            user['email'], 
            user['password'], 
            **create_data
        )
        assert CompanyProfile.objects.filter(uuid=tested_company.uuid).exists()
        assert tested_company.user.username == user['username']
        assert tested_company.user.creator == admin_user


@pytest.mark.django_db
class TestCreateEmployee():

    def setup_method(self, method):
        self.expected_username = fake.user_name()
        self.expected_password = fake.password()
        self.expected_email = fake.email()
        self.expected_branch = factories.BranchFactory.create()
        self.expected_position = factories.PositionFactory.create()
        self.create_data = generate_to_dict(factories.EmployeeProfileFactory)
        self.create_data.pop('user')
        self.create_data.pop('branch')
        self.create_data.pop('position')

    def test_create(self, admin_user):
        employee = utils.create_employee(
            admin_user,
            self.expected_username,
            self.expected_email,
            self.expected_password,
            branch_uuid=self.expected_branch.uuid,
            position_uuid=self.expected_position.uuid,
            **self.create_data
        )
        employee_user = get_user_model().employee_objects.get(username=self.expected_username)
        assert check_password(self.expected_password, employee_user.password)
        assert EmployeeProfile.objects.filter(uuid=employee.uuid).exists()
        assert employee.user.creator == admin_user

    def test_create_atomic(self, mocker, admin_user):
        mock_create = mocker.patch('companies.utils.EmployeeProfile.objects.create')
        mock_create.side_effect = Exception
        with pytest.raises(Exception):
            employee = utils.create_employee(
                admin_user,
                self.expected_username,
                self.expected_password,
                branch_uuid=self.expected_branch.uuid,
                position_uuid=self.expected_position.uuid,
                **self.create_data
            )
        assert not get_user_model().employee_objects.filter(username=self.expected_username).exists()

@pytest.mark.django_db
class TestEmployeeToArchive():

    def setup_method(self, method):
        self.employee = factories.EmployeeProfileFactory.create()

    def test_to_archive(self):
        utils.employee_to_archive(self.employee.uuid)
        self.employee.refresh_from_db()
        assert self.employee.status == Statuses.ARCHIVED
        assert not self.employee.user.is_active

    def test_to_archive_atomic(self, mocker):
        mock_to_archive = mocker.patch('companies.utils.EmployeeProfile.to_archive')
        mock_to_archive.side_effect = Exception
        with pytest.raises(Exception):
            utils.employee_to_archive(self.employee.uuid)
        assert not self.employee.status == Statuses.ARCHIVED
        assert self.employee.user.is_active


@pytest.mark.django_db
class TestEmployeeToWork():

    def setup_method(self, method):
        self.employee = factories.EmployeeProfileFactory.create(status=Statuses.ARCHIVED)
        self.employee.user.deactivate()

    def test_call_validator(self, mocker):
        mock_validate = mocker.patch('companies.utils.validators.validate_employee_to_work')
        mock_validate.side_effect = ValidationError(Exception)
        with pytest.raises(ValidationError):
            utils.employee_to_work(self.employee.uuid)
        mock_validate.assert_called_with(self.employee)

    def test_to_work_atomic(self, mocker):
        mock_activate = mocker.patch('accounts.models.UserAccount.activate')
        mock_activate.side_effect = Exception
        with pytest.raises(Exception):
            utils.employee_to_work(self.employee.uuid)
        self.employee.refresh_from_db()
        assert self.employee.status == Statuses.ARCHIVED

    def test_to_work_and_activate_user(self, mocker):
        mock_validate = mocker.patch('companies.utils.validators.validate_employee_to_work')
        mock_validate.return_value = True
        utils.employee_to_work(self.employee.uuid)
        self.employee.refresh_from_db()
        assert self.employee.status == Statuses.WORKS
        assert self.employee.user.is_active

    
@pytest.mark.django_db
class TestBranchToArchive():

    def setup_method(self, method):
        self.branch = factories.BranchFactory.create(status=Statuses.WORKS)

    def test_with_force(self, mocker):
        mock_validate = mocker.patch('companies.utils.validators.validate_branch_to_archive')
        utils.branch_to_archive(self.branch.uuid, force=True)
        mock_validate.call_count == 0

    def test_with_no_employees(self, mocker):
        utils.branch_to_archive(self.branch.uuid)
        self.branch.refresh_from_db()
        assert self.branch.status == Statuses.ARCHIVED

    def test_to_archive_atomic(self, mocker):
        employee = factories.EmployeeProfileFactory.create(branch=self.branch, status=Statuses.WORKS)
        mock_archive = mocker.patch('companies.utils.employee_to_archive')
        mock_archive.side_effect = Exception
        with pytest.raises(Exception):
            utils.branch_to_archive(self.branch.uuid)
        self.branch.refresh_from_db()
        assert self.branch.status == Statuses.WORKS

    def test_to_archive_with_employees(self, mocker):
        factories.EmployeeProfileFactory.create_batch(3, branch=self.branch, status=Statuses.WORKS)
        mock_validate = mocker.patch('companies.utils.validators.validate_branch_to_archive')
        utils.branch_to_archive(self.branch.uuid)
        self.branch.refresh_from_db()
        assert self.branch.status == Statuses.ARCHIVED
        assert not EmployeeProfile.objects.filter(status=Statuses.WORKS).exists()


@pytest.mark.django_db
class TestBranchToWork():

    def test_validate_branch(self, mocker):
        branch = factories.BranchFactory.create(status=Statuses.ARCHIVED)
        mock_validate = mocker.patch('companies.utils.validators.validate_branch_to_work')
        utils.branch_to_work(branch.uuid)
        branch.refresh_from_db()
        assert branch.status == Statuses.WORKS
        mock_validate.assert_called_with(branch)


@pytest.mark.django_db
class TestCompanyToArchive():

    def setup_method(self, method):
        self.company = factories.CompanyProfileFactory.create(status=Statuses.WORKS)

    def test_with_force(self, mocker):
        mock_validate = mocker.patch('companies.utils.validators.validate_company_to_archive')
        utils.company_to_archive(self.company.uuid, force=True)
        mock_validate.call_count == 0

    def test_with_no_branches(self, mocker):
        mock_archivate = mocker.patch('companies.utils.branch_to_archive')
        utils.company_to_archive(self.company.uuid)
        self.company.refresh_from_db()
        assert mock_archivate.call_count == 0
        assert self.company.status == Statuses.ARCHIVED
        assert not self.company.user.is_active

    def test_with_branches(self, mocker):
        branch = factories.BranchFactory(company=self.company, status=Statuses.WORKS)
        mock_archivate = mocker.patch('companies.utils.branch_to_archive')
        utils.company_to_archive(self.company.uuid)
        self.company.refresh_from_db()
        branch.refresh_from_db()
        mock_archivate.assert_called_with(branch.uuid, force=False)
        assert self.company.status == Statuses.ARCHIVED
        assert not self.company.user.is_active

    def test_to_archive_atomic(self, mocker):
        mock_deactivate = mocker.patch('accounts.models.UserAccount.deactivate')
        mock_deactivate.side_effect = Exception
        with pytest.raises(Exception):
            utils.company_to_archive(self.company.uuid)
        assert self.company.status == Statuses.WORKS
        assert self.company.user.is_active


@pytest.mark.django_db
class TestCompanyToWork():

    def setup_method(self, method):
        self.company = factories.CompanyProfileFactory.create(status=Statuses.ARCHIVED)
        self.company.user.deactivate()

    def test_to_work(self):
        utils.company_to_work(self.company.uuid)
        self.company.refresh_from_db()
        assert self.company.status == Statuses.WORKS
        assert self.company.user.is_active
    
    def test_to_work_atomic(self, mocker):
        mock_activate = mocker.patch('accounts.models.UserAccount.activate')
        mock_activate.side_effect = Exception
        with pytest.raises(Exception):
            utils.company_to_work(self.company.uuid)
        assert self.company.status == Statuses.ARCHIVED
        assert not self.company.user.is_active


@pytest.mark.django_db
class TestDeleteEmployee():

    def setup_method(self, method):
        self.employee = factories.EmployeeProfileFactory.create()

    def test_delete(self):
        utils.delete_employee(self.employee.uuid)
        assert not EmployeeProfile.objects.filter(uuid=self.employee.uuid).exists()
        assert not get_user_model().objects.filter(uuid=self.employee.user.uuid).exists()

    def test_delete_atomic(self, mocker):
        mock_delete = mocker.patch('accounts.models.UserAccount.delete')
        mock_delete.side_effect = Exception
        with pytest.raises(Exception):
            utils.delete_employee(self.employee.uuid)
        assert EmployeeProfile.objects.filter(uuid=self.employee.uuid).exists()
        assert get_user_model().objects.filter(uuid=self.employee.user.uuid).exists()


@pytest.mark.django_db
class TestDeleteBranch():

    def setup_method(self, method):
        self.branch = factories.BranchFactory.create()

    def test_delete_with_no_employees(self, mocker):
        mock_delete = mocker.patch('companies.utils.delete_employee')
        utils.delete_branch(self.branch.uuid)
        assert mock_delete.call_count == 0
        assert not Branch.objects.filter(uuid=self.branch.uuid).exists()

    def test_delete_with_employees(self, mocker):
        factories.EmployeeProfileFactory.create_batch(3, branch=self.branch)
        utils.delete_branch(self.branch.uuid)
        assert not Branch.objects.filter(uuid=self.branch.uuid).exists()
        assert not EmployeeProfile.objects.filter(branch=self.branch).exists()

    def test_delete_atomic(self, mocker):
        employee = factories.EmployeeProfileFactory.create(branch=self.branch)
        mock_delete = mocker.patch('companies.utils.Branch.delete')
        mock_delete.side_effect = Exception
        with pytest.raises(Exception):
            utils.delete_employee(self.employee.uuid)
        assert Branch.objects.filter(uuid=self.branch.uuid).exists()
        assert EmployeeProfile.objects.filter(uuid=employee.uuid).exists()


@pytest.mark.django_db
class TestDeleteCompany():

    def setup_method(self, method):
        self.company = factories.CompanyProfileFactory.create()

    def test_delete_with_no_branches(self, mocker):
        mock_delete = mocker.patch('companies.utils.delete_branch')
        utils.delete_company(self.company.uuid)
        assert mock_delete.call_count == 0
        assert not CompanyProfile.objects.filter(uuid=self.company.uuid).exists()
        assert not get_user_model().objects.filter(uuid=self.company.user.uuid).exists()

    def test_delete_with_branches(self, mocker):
        factories.BranchFactory.create_batch(3, company=self.company)
        utils.delete_company(self.company.uuid)
        assert not CompanyProfile.objects.filter(uuid=self.company.uuid).exists()
        assert not Branch.objects.filter(company=self.company).exists()
        assert not get_user_model().objects.filter(uuid=self.company.user.uuid).exists()

    def test_delete_atomic(self, mocker):
        branch = factories.BranchFactory.create(company=self.company)
        mock_delete = mocker.patch('accounts.models.UserAccount.delete')
        mock_delete.side_effect = Exception
        with pytest.raises(Exception):
            utils.delete_company(self.company.uuid)
        assert CompanyProfile.objects.filter(uuid=self.company.uuid).exists()
        assert Branch.objects.filter(company=self.company).exists()
        assert get_user_model().objects.filter(uuid=self.company.user.uuid).exists()


@pytest.mark.django_db
class TestChangeEmployeePosition():

    def test_change_position(self):
        old_position = factories.PositionFactory.create()
        new_position = factories.PositionFactory.create()
        employee = factories.EmployeeProfileFactory.create(position=old_position)
        utils.change_employee_position(employee.uuid, new_position.uuid)
        employee.refresh_from_db()
        assert employee.position == new_position
        assert employee.position == new_position


@pytest.mark.django_db
class TestTransferEmployeeToBranch():

    def test_transfer(self):
        old_branch = factories.BranchFactory.create()
        new_branch = factories.BranchFactory.create()
        employee = factories.EmployeeProfileFactory.create(branch=old_branch)
        utils.transfer_employee_to_branch(employee.uuid, new_branch.uuid)
        employee.refresh_from_db()
        assert employee.branch == new_branch


@pytest.mark.django_db
class TestCreateToBranch():

    def setup_method(self, method):
        self.expected_company = factories.CompanyProfileFactory.create()
        self.create_data = generate_to_dict(factories.BranchFactory)
        self.create_data.pop('company')

    def test_create(self):
        utils.create_branch(self.expected_company.uuid, **self.create_data)
        expected_branch = Branch.objects.get(**self.create_data)
        assert expected_branch.company == self.expected_company

    def test_with_company_does_not_exist(self):
        company_uuid = fake.uuid4()
        with pytest.raises(CompanyProfile.DoesNotExist):
            utils.create_branch(company_uuid, **self.create_data)
