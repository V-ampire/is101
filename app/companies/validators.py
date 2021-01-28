from django.core.exceptions import ValidationError

from accounts.utils import is_company_user, is_employee_user


def validate_company_user(user):
    """
    Проверяет что у пользователя роль Юрлица.
    """
    if not is_company_user(user):
        raise ValidationError(f"Учетная запись не может быть использована для профиля юрлица")


def validate_employee_user(user):
    """
    Проверяет что у пользователя роль работника.
    """
    if not is_employee_user(user):
        raise ValidationError(f"Учетная запись не может быть использована для профиля работника")