from rest_framework.serializers import ValidationError

from companies.models import Branch, EmployeeProfile, Position


def validate_user_data(**user_data):
    """
    Проверяем существует ли такая учетная запись.
    Проверяем что учетная запись имеет роль работника.
    """
    try:
        user = get_user_model().objects.get(**user_data)
    except get_user_model().DoesNotExist:
        raise ValidationError('Учетная запись не зарегистрирована')
    
    if user.role != Roles.EMPLOYEE:
        raise ValidationError(
            f'Учетная запись {user.username} не может быть использована для работника'
        )
    return user


def validate_user_data_for_create(**user_data):
    """
    Проверяем существует ли такая учетная запись.
    Проверяем что учетная запись имеет роль работника.
    Проверяем не привязан ли к учетной записи работник.
    """
    user = validate_user_data(**user_data)
    if hasattr(user, 'employee'):
        raise ValidationError(
            f'На учетную запись {user.username} уже оформлен работник {user.employee.fio}'
        )
    return user


def validate_branch_for_transfer(branch_uuid, employee_uuid):
    """
    Филиал не должен принадлежать другому юрлицу.
    Филиал не должен быть в архиве.
    """
    try:
        branch = Branch.objects.get(uuid=branch_uuid)
        if branch.status == Branch.ARCHIVED:
            raise ValidationError(f'Невозможно перевести работника - филиал {branch.title} в архиве.')
    except Branch.DoesNotExist:
        raise alidationError(f'Филиал не существует.')
    
    try:
        employee = Employee.objects.get(uuid=employee_uuid)
        if employee.branch.company != branch.company:
            raise ValidationError(f'Невозможно перевести работника в филиал другого юрлица.')
    except Employee.DoesNotExist:
        raise ValidationError('Информация о работнике отсутствует.')

    return branch_uuid


def validate_position_for_change(position_uuid):
    try:
        position = Position.objects.get(uuid=position_uuid)
    except Position.DoesNotExist:
        raise ValidationError('Должность не существует.')

    if position.status == Position.ARCHIVED:
        raise ValidationError('Должность находится в архиве.')

    return position_uuid
