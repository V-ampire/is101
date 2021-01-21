from rest_framework.serializers import ValidationError


def validate_user_employee_to_activate(user):
    """
    Учетную запись работника можно активировать только после 
    добавления информации о работнике.
    Если валидация пройдена вернет True.
    """
    try:
        if user.employee:
           return True
    except AttributeError:
        msg = f'Учетная запись {user.username} не активирована. Заполните профиль работника.'
        raise ValidationError(msg)