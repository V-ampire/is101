from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def is_user_company(user_uuid):
    """
    Проверяет что учетная запись принадлежит компании.
    """
    user = get_user_model().objects.get(uuid=user_uuid)

    if user.role != get_user_model().COMPANY:
        raise ValidationError(
            _('User role is not %(company)s.'), 
            params={'company': get_user_model().COMPANY}
        )


def is_user_employee(user_uuid):
    """
    Проверяет что учетная запись принадлежит работнику.
    """
    user = get_user_model().objects.get(uuid=user_uuid)

    if user.role != get_user_model().EMPLOYEE:
        raise ValidationError(
            _('User role is not %(employee)s.'), 
            params={'employee': get_user_model().EMPLOYEE}
        )


def validate_user_employee_to_activate(user_uuid):
    """
    Учетную запись работника можно активировать только после 
    добавления информации о работнике.
    Если валидация пройдена вернет True.
    """
    try:
        user = get_user_model().employee_objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        raise ValidationError('Учетная запись для работника не существует.')

    try:
        if user.employee:
           return True
    except AttributeError:
        msg = f'Учетная запись {user.username} не активирована. Заполните профиль работника.'
        raise ValidationError(msg)