from rest_framework.serializers import ValidationError

from api.v1.employees import serializers

from companies.factories import EmployeeProfileFactory, BranchFactory, PositionFactory


from factory_generator import generate_to_dict
from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestCreateEmployeeSerializer():

    def setup_method(self, method):
        self.create_data = generate_to_dict(EmployeeProfileFactory)


    def test_validate_calls_validate_user(self, mocker):
        mock_is_valid_user = mocker.patch('api.v1.employees.serializers.EmployeeUserAccountSerializer.is_valid')
        self.expected_branch = BranchFactory.create()
        self.expected_position = PositionFactory.create()
        self.create_data.pop('user')
        self.create_data.pop('employee_position')
        self.create_data['branch'] = self.expected_branch.uuid
        self.create_data['position'] = self.expected_position.uuid
        self.create_data['username'] = fake.user_name()
        self.create_data['password'] = fake.password()

    def test_call_validate_user(self, mocker):
        mock_validate_user = mocker.patch(
            'api.v1.employees.serializers.EmployeeUserAccountSerializer.is_valid'
        )
        serializer = serializers.EmployeeCreateSerializer()
        result = serializer.validate(self.create_data)
        mock_validate_user.assert_called_with(raise_exception=True)
        assert result == self.create_data

    def test_user_validation_data(self, mocker):
        mock_run_validation_user = mocker.patch(
            'api.v1.employees.serializers.EmployeeUserAccountSerializer.run_validation'
        )
        serializer = serializers.EmployeeCreateSerializer()
        serializer.validate(self.create_data)
        mock_run_validation_user.assert_called_with(
            {'username': self.create_data['username'], 'password': self.create_data['password']}
        )

    def test_create(self, mocker):
        expected_employee = mocker.Mock()
        mock_create = mocker.patch('api.v1.employees.serializers.utils.create_employee')
        mock_create.return_value = expected_employee
        serializer = serializers.EmployeeCreateSerializer()
        expected_username = self.create_data['username']
        expected_password = self.create_data['password']
        expected_branch_uuid = self.create_data['branch']
        expected_position = self.create_data['position']
        result = serializer.create(self.create_data)
        mock_create.assert_called_with(
            expected_username,
            expected_password,
            expected_branch_uuid,
            position_uuid=expected_position,
            **self.create_data
        )
        assert result == expected_employee


@pytest.mark.django_db
class TestChangePositionSerializer():

    def test_validate_uuid(self, mocker):
        expected_position = PositionFactory.create()
        mock_validate = mocker.patch('api.v1.employees.serializers.validators.validate_position_for_change')
        mock_validate.return_value = expected_position.uuid
        serializer = serializers.ChangePositionSerializer()
        result = serializer.validate_position(expected_position.uuid)
        mock_validate.assert_called_with(expected_position)
        assert result == expected_position.uuid

    def test_validate_with_invalid_uuid(self):
        invalid_uuid = fake.uuid4()
        serializer = serializers.ChangePositionSerializer()
        exp_message = f'Должность с uuid={invalid_uuid} не существует.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            serializer.validate_position(invalid_uuid)
        assert exc_info.value.args[0] == exp_message


@pytest.mark.django_db
class TestChangeBranchSerializer():

    def test_validate_with_branch_doesnt_exists(self):
        branch_uuid = fake.uuid4()
        employee = EmployeeProfileFactory.create()
        serializer = serializers.ChangeBranchSerializer()
        exp_message = f'Филиал с uuid={branch_uuid} не существует.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            serializer.validate({'branch': branch_uuid, 'employee': employee.uuid})
        assert exc_info.value.args[0] == exp_message

    def test_validate_with_employee_doesnt_exists(self):
        employee_uuid = fake.uuid4()
        branch = BranchFactory.create()
        serializer = serializers.ChangeBranchSerializer()
        exp_message = f'Работник с uuid={employee_uuid} не существует.'
        with pytest.raises(ValidationError) as exc:
            exc_info = exc
            serializer.validate({'branch': branch.uuid, 'employee': employee_uuid})
        assert exc_info.value.args[0] == exp_message

    def test_validate(self, mocker):
        expected_branch = BranchFactory.create()
        expected_employee = EmployeeProfileFactory.create()
        expected_data = {
            'branch': expected_branch.uuid,
            'employee': expected_employee.uuid
        }
        mock_validate = mocker.patch('api.v1.employees.serializers.validators.validate_branch_for_transfer')
        serializer = serializers.ChangeBranchSerializer()
        result = serializer.validate(expected_data)
        mock_validate.assert_called_with(expected_branch, expected_employee)
        assert result == expected_data

