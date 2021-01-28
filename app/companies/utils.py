from django.contrib.auth import get_user_model
from django.db import transaction

from company.models import CompanyProfile, EmployeeProfile, Position, Branch

import logging


logger = logging.getLogger(__name__)


def has_user_perm_to_company(company_uuid, user_uuid):
    """
    Проверяет имеет ли учетная запись доступ к информации о юрлице.
    """
    try:
        user = get_user_model().objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Пользователь с uuid={user_uuid} не существует.")
        return False
    try:
        company = CompanyProfile.objects.get(uuid=company_uuid)
    except CompanyProfile.DoesNotExist:
        logger.warning(f"Проверка доступа для несуществующей компании company_uuid={company_uuid}")
        return False
    return company.user.uuid == user_uuid or user.is_staff


def has_user_perm_to_branch(branch_uuid, user_uuid):
    """
    Проверяет имеет ли учетная запись доступ к информации о филиале.
    """
    try:
        user = get_user_model().objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Пользователь с uuid={user_uuid} не существует.")
        return False
    try:
        branch = Branch.objects.get(uuid=branch_uuid)
    except Branch.DoesNotExist:
        logger.warning(f"Проверка доступа для несуществующей компании company_uuid={company_uuid}")
        return False
    return branch.company.user.uuid == user_uuid or user.is_staff


def has_user_perm_to_employee(employee_uuid, user_uuid):
    """
    Проверяет имеет ли учетная запись доступ к информации о работнике.
    """
    try:
        user = get_user_model().objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Пользователь с uuid={user_uuid} не существует.")
        return False
    try:
        employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    except EmployeeProfile.DoesNotExist:
        logger.warning(f"Проверка доступа для несуществующей компании company_uuid={company_uuid}")
        return False
    return employee.branch.company.user.uuid == user_uuid or user.is_staff


def delete_company(company_uuid):
    """
    Удаление юрлица.
    Вместе с юрлицом удаляется его учетная запись.
    """
    with transaction.atomic():
        company = CompanyProfile.objects.get(uuid=company_uuid)
        user = company.user
        company.delete()
        user.delete()


def company_to_archive(company_uuid):
    """
    Перевод юрлица в архивный статус.
    Одновременно деактивирует учетную запись.
    """
    with transaction.atomic():
        company = CompanyProfile.objects.get(uuid=company_uuid)
        user = company.user
        company.to_archive()
        user.deactivate()


def company_to_work(company_uuid):
    """
    Перевод юрлица в активный статус.
    Одновременно ативирует учетную запись.
    """
    with transaction.atomic():
        company = CompanyProfile.objects.get(uuid=company_uuid)
        user = company.user
        company.to_work()
        user.activate()


def create_company(user_uuid, **company_data):
    """
    Создать юрлицо.
    :param user_uuid: UUID созданной учетной записи с ролью Юрлица.
    """
    user = get_user_model().company_objects.get(uuid=user_uuid)
    return CompanyProfile.objects.create(user=user, **company_data)


def create_employee(username, password, **employee_data):
    """
    Создать учетку работника.
    Создать профиль работника.
    """
    with transaction.atomic():
        user = get_user_model().employee_objects.create_user(username=username, password=password)
        return EmployeeProfile.objects.create(user=user, **employee_data)


def change_employee_position(employee_uuid, new_position_uuid):
    """
    Изменить должность работника.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    new_position = Position.objects.get(uuid=new_position_uuid)
    employee.employee_position = new_position
    employee.save()
    return employee


def transfer_employee_to_branch(employee_uuid, branch_uuid):
    """
    Переводит работника в указанный филиал.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    new_branch = Branch.objects.get(uuid=branch_uuid)
    employee.branch = new_branch
    employee.save()
    return employee