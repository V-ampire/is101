from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def is_user_company(user_pk):
    """
    Проверяет что учетная запись принадлежит компании.
    """
    user = get_user_model().objects.get(pk=user_pk)

    if user.role != get_user_model().COMPANY:
        raise ValidationError(
            _('User role is not %(company)s.'), 
            params={'company': get_user_model().COMPANY}
        )


def is_user_employee(user_pk):
    """
    Проверяет что учетная запись принадлежит работнику.
    """
    user = get_user_model().objects.get(pk=user_pk)

    if user.role != get_user_model().EMPLOYEE:
        raise ValidationError(
            _('User role is not %(employee)s.'), 
            params={'employee': get_user_model().EMPLOYEE}
        )