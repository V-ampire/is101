from django.contrib.auth import get_user_model

from accounts.factories import CompanyUserAccountModelFactory

from company.factories import CompanyFactory, BranchFactory, EmployeeFactory
from company.models import Company, Employee,  Branch
from company import utils
from company.exceptions import IncorrectObjectState

from factory_generator import generate_to_dict, generate_to_db
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestDeleteCompany():

    def setup_method(self, method):
        self.company = CompanyFactory.create()
        self.user = self.company.user

    def test_delete_company(self):
        utils.delete_company(self.company.uuid)
        assert not Company.objects.filter(uuid=self.company.uuid).exists()
        assert not get_user_model().objects.filter(uuid=self.user.uuid).exists()

    def test_atomic_delete_with_user(self, mocker):
        mock_user_delete = mocker.patch('accounts.models.UserAccount.delete')
        mock_user_delete.side_effect = Exception
        with pytest.raises(Exception):
            utils.delete_company(self.company.uuid)
        assert Company.objects.filter(uuid=self.company.uuid).exists()
        assert get_user_model().objects.filter(uuid=self.user.uuid).exists()


@pytest.mark.django_db
class TestArchivateCompany():

    def setup_method(self, method):
        self.company = CompanyFactory.create()
        self.user = self.company.user

    def test_archivate_company(self):
        utils.archivate_company(self.company.uuid)
        self.company.refresh_from_db()
        self.user.refresh_from_db()
        assert self.company.status == Company.ARCHIVED
        assert not self.user.is_active

    def test_archivate_company_atomic_with_user(self, mocker):
        mock_user_deactivate = mocker.patch('accounts.models.UserAccount.deactivate')
        mock_user_deactivate.side_effect = Exception
        with pytest.raises(Exception):
            utils.archivate_company(self.company.uuid)
        self.company.refresh_from_db()
        self.user.refresh_from_db()
        assert self.company.status == Company.ACTIVE
        assert self.user.is_active

    
@pytest.mark.django_db
class TestActivateCompany():

    def setup_method(self, method):
        self.company = CompanyFactory.create(status=Company.ARCHIVED)
        self.user = self.company.user
        self.user.deactivate()

    def test_activate_company(self):
        utils.activate_company(self.company.uuid)
        self.company.refresh_from_db()
        self.user.refresh_from_db()
        assert self.company.status == Company.ACTIVE
        assert self.user.is_active

    def test_activate_company_atomic_with_user(self, mocker):
        mock_user_activate = mocker.patch('accounts.models.UserAccount.activate')
        mock_user_activate.side_effect = Exception
        with pytest.raises(Exception):
            utils.activate_company(self.company.uuid)
        self.company.refresh_from_db()
        self.user.refresh_from_db()
        assert self.company.status == Company.ARCHIVED
        assert not self.user.is_active


@pytest.mark.django_db
class TestCreateCompany():

    def setup_method(self, method):
        self.user = CompanyUserAccountModelFactory.create()
        self.create_data = generate_to_dict(CompanyFactory)
        self.create_data.pop('user')

    def test_create(self):
        tested_company = utils.create_company(self.user.uuid, **self.create_data)
        assert Company.objects.filter(uuid=tested_company.uuid).exists()
        assert tested_company.user == self.user


@pytest.mark.django_db
class TestArchivateBranch():

    def setup_method(self):
        self.tested_branch = BranchFactory()

    def test_archivate_without_employees(self):
        result = utils.archivate_branch(self.tested_branch.uuid)
        self.tested_branch.refresh_from_db()
        assert self.tested_branch.status == Employee.ARCHIVED
        assert result.uuid == self.tested_branch.uuid

    def test_archivate_with_active_employees(self):
        generate_to_db(EmployeeFactory, quantity=5, status=Employee.ACTIVE, 
                        branch=self.tested_branch)
        with pytest.raises(IncorrectObjectState):
            utils.archivate_branch(self.tested_branch.uuid)

    def test_archivate(self):
        generate_to_db(EmployeeFactory, quantity=5, status=Employee.ARCHIVED, 
                        branch=self.tested_branch)
        result = utils.archivate_branch(self.tested_branch.uuid)
        self.tested_branch.refresh_from_db()
        assert self.tested_branch.status == Employee.ARCHIVED
        assert result.uuid == self.tested_branch.uuid


@pytest.mark.django_db
class TestActivateBranch():

    def test_activate(self):
        branch = BranchFactory.create(status=Branch.ARCHIVED)
        utils.activate_branch(branch_uuid)
        branch.refresh_from_db()
        assert branch.status == Branch.ACTIVE