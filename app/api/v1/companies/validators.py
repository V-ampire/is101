from django.contrib.auth import get_user_model

from rest_framework.serializers import ValidationError


def validate_user_data(**user_data):
    """
    Проверяем существует ли такая учетная запись.
    Проверяем что учетная запись имеет роль юрлица.
    """
    try:
        user = get_user_model().objects.get(**user_data)
    except get_user_model().DoesNotExist:
        raise ValidationError('Учетная запись не зарегистрирована')
    
    if user.role != get_user_model().COMPANY:
        raise ValidationError(
            f'Учетная запись {user.username} не может быть использована для юрлица'
        )
    return user


def validate_user_data_for_create(**user_data):
    """
    Проверяем существует ли такая учетная запись.
    Проверяем что учетная запись имеет роль юрлица.
    Проверяем не привязано ли к учетной записи юрлицо.
    """
    user = validate_user_data(**user_data)
    if hasattr(user, 'company'):
        raise ValidationError(
            f'На учетную запись {user.username} уже оформлено юрлицо {user.company.title}'
        )
    return user