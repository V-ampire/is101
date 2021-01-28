from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from companies.models import CompanyProfile, EmployeeProfile, Position, Branch
from companies import validators

import logging


logger = logging.getLogger(__name__)


def has_user_perm_to_company(company_uuid, user_uuid):
    """
    Проверяет имеет ли учетная запись доступ к информации о юрлице.
    Доступ имеют админы и владелец.
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
    Доступ имеют админы и юрлицо владелец.
    """
    try:
        user = get_user_model().objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Пользователь с uuid={user_uuid} не существует.")
        return False
    try:
        branch = Branch.objects.get(uuid=branch_uuid)
    except Branch.DoesNotExist:
        logger.warning(f"Проверка доступа для несуществующего филиала branch_uuid={branch_uuid}")
        return False
    return branch.company.user.uuid == user_uuid or user.is_staff


def has_user_perm_to_employee(employee_uuid, user_uuid):
    """
    Проверяет имеет ли учетная запись доступ к информации о работнике.
    Доступ имеют админы и юрлицо владелец.
    """
    try:
        user = get_user_model().objects.get(uuid=user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Пользователь с uuid={user_uuid} не существует.")
        return False
    try:
        employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    except EmployeeProfile.DoesNotExist:
        logger.warning(f"Проверка доступа для несуществующего работника employee_uuid={employee_uuid}")
        return False
    return employee.branch.company.user.uuid == user_uuid or user.is_staff


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


def employee_to_archive(employee_uuid):
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    user = employee.user
    with transaction.atomic():
        employee.to_archive()
        user.deactivate()


def employee_to_work(employee_uuid):
    """
    Перевод работника в статус Работает.
    Активация учетной записи.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    validators.validate_employee_to_work(employee)
    with transaction.atomic():
        employee.to_work()
        employee.user.activate()


def branch_to_archive(branch_uuid, force=False):
    """
    Перевод филиала в архивный статус.
    :param force: Флаг указывающий на принудительное архивирование работников.
    Если не указан и на филиале числятся работники со статусом Работает то будет выброшена ошибка валидации.
    """
    branch = Branch.objects.get(uuid=company_uuid)
    if not force:
        validators.validate_branch_to_archive(branch)
    with transaction.atomic():
        try:
            for employee in branch.employees.all():
                employee_to_archive(employee.uuid)
                employee.to_archive()
        except ObjectDoesNotExist:
            pass
        branch.to_archive()


def branch_to_work(branch_uuid):
    """
    Перевод филиала в статус Работает.
    Работники остаются в архиве.
    """
    branch = Branch.objects.get(uuid=branch_uuid)
    validators.validate_branch_to_work(branch)
    branch.to_work()


def company_to_archive(company_uuid, force=False):
    """
    Перевод юрлица в архивный статус.
    Одновременно деактивирует учетную запись.
    Архивируются все филиалы.
    :param force: Флаг указывающий на принудительное архивирование работников.
    Если не указан и на юрлице числятся работники со статусом Работает то будет выброшена ошибка валидации.
    """
    company = CompanyProfile.objects.get(uuid=company_uuid)
    if not force:
        validators.validate_company_to_archive(company)
    with transaction.atomic():
        user = company.user
        try:
            for branch in company.branches.all():
                branch_to_archive(branch.uuid, force=force)
        except ObjectDoesNotExist:
            pass
        company.to_archive()
        user.deactivate()


def company_to_work(company_uuid):
    """
    Перевод юрлица в статус Работает.
    Филиалы и работники остаются в архиве.
    Активирование учетной записи
    """
    company = CompanyProfile.objects.get(uuid=company_uuid)
    with transaction.atomic():
        company.to_work()
        company.activate()


def delete_employee(employee_uuid):
    """
    Удаление работника.
    Вместе с работником удаляется его учетная запись.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    user = employee.user
    with transaction.atomic():
        user = employee.user
        employee.delete()
        user.delete()


def delete_branch(branch_uuid):
    """
    Удаление филиала.
    Вместе с филиалом удаляются все работники.
    """
    with transaction.atomic():
        branch = Branch.objects.get(uuid=branch_uuid)
        try:
            for employee in  branch.employees.all():
                delete_employee(employee.uuid)
        except ObjectDoesNotExist:
            pass
        branch.delete()


def delete_company(company_uuid):
    """
    Удаление юрлица.
    Вместе с юрлицом удаляется его учетная запись.
    Удаляются все филиалы с работниками.
    """
    company = CompanyProfile.objects.get(uuid=company_uuid)
    user = company.user
    with transaction.atomic():
        try:
            for branch in company.branches.all():
                delete_branch(branch.uuid)
        company.delete()
        user.delete()


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