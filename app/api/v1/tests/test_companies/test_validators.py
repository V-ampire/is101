from rest_framework.serializers import ValidationError

from api.v1.companies import validators

from company.factories import CompanyFactory

from faker import Faker
import pytest


fake = Faker()


@pytest.mark.django_db
class TestValidateUserData():

    def test_validate_user_if_user_doesnt_exist(self):
        """
        Тест случая когда учетная запись не существует.
        """
        user_data = {
            'username': fake.user_name(),
            'uuid': fake.uuid4()
        }
        expected_msg = 'Учетная запись не зарегистрирована'
        with pytest.raises(ValidationError, match=expected_msg):
            validators.validate_user_data(**user_data)

    def test_validate_user_isnot_company_user(self, employee_user):
        """
        Тест случая когда роль учетной записи не юрлицо.
        """
        user_data = {
            'username': employee_user.username,
            'uuid': employee_user.uuid
        }
        expected_msg = f'Учетная запись {user_data.get("username")} не может быть использована для юрлица'
        with pytest.raises(ValidationError, match=expected_msg):
            validators.validate_user_data(**user_data)

    def test_validate_user_success(self, company_user):
        user_data = {
            'username': company_user.username,
            'uuid': company_user.uuid
        }
        expected_pk = company_user
        tested_user = validators.validate_user_data(**user_data)
        assert company_user == tested_user


@pytest.mark.django_db
class TestValidateUserDataForCreate():

    def test_validate_user_company_exist(self, mocker):
        """
        Тест случая когда к учетной записи уже привязано юрлицо.
        """
        company = CompanyFactory()
        mock_validate = mocker.patch('api.v1.companies.validators.validate_user_data')
        mock_validate.return_value = company.user
        user_data = {
            'username': company.user.username,
            'uuid': company.user.uuid
        }
        expected_msg = f'На учетную запись {company.user.username} уже оформлено юрлицо {company.title}'
        with pytest.raises(ValidationError, match=expected_msg):
            validators.validate_user_data_for_create(**user_data)
        assert mock_validate.call_count == 1
        mock_validate.assert_called_with(**user_data)
            
    def test_validate_user_success(self, mocker, company_user):
        user_data = {
            'username': company_user.username,
            'uuid': company_user.uuid
        }
        expected_pk = company_user
        tested_user = validators.validate_user_data_for_create(**user_data)
        assert company_user == tested_user




