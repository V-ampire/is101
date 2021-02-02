from django.core.exceptions import ValidationError, ObjectDoesNotExist

from accounts.utils import is_company_user, is_employee_user

from core.models import Statuses


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


def validate_company_to_archive(company):
    """
    Валидация профлия юрлица перед переводом в архив.
    Юрлицо не должно иметь работников в рабочем статусе.
    """
    try:
        for branch in company.branches.all():
            if branch.employees.filter(status=Statuses.WORKS).exists():
                raise ValidationError(
                    f'Невозможно перевести юрлицо {company.title} в архив пока в нем числятся работающие сотрудники.'
                )
    except ObjectDoesNotExist:
        # Нет филиалов или работников в филиалах
        pass


def validate_branch_to_archive(branch):
    """
    Валидация филиала юрлица перед переводом в архив.
    Филиал не должен иметь работников в рабочем статусе.
    """
    try:
        if branch.employees.filter(status=Statuses.WORKS).exists():
            raise ValidationError(
                f'Невозможно перевести филиал {branch} в архив пока в нем числятся работающие сотрудники.'
            )
    except ObjectDoesNotExist:
        # Нет работников в филиале
        pass


def validate_branch_to_work(branch):
    """
    Валидация филиала перед переводом в статус Работает.
    Филиал не может быть переведен в рабочий статус если юрлицо в архиве.
    """
    if branch.company.status == Statuses.ARCHIVED:
        raise ValidationError(
            f'Невозможно перевести филиал {branch} в рабочий статус пока архивировано юрлицо {branch.company.title}.'
        )


def validate_employee_to_work(employee):
    """
    Валидация работника перед переводом в статс Работает.
    работник не может быть переведен в рабочий статус если филиал или юрлицо в архиве.
    """
    if employee.branch.status == Statuses.ARCHIVED or employee.branch.company.status == Statuses.ARCHIVED:
        raise ValidationError(
            f'Невозможно перевести работника {employee.fio} в рабочий статус '
            f'пока архивирован филиал {employee.branch} '
            f'или юрлицо {employee.branch.company.title}.'
        )


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