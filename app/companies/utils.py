from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from companies.models import CompanyProfile, EmployeeProfile, Position, Branch
from companies import validators

import logging


logger = logging.getLogger(__name__)


def create_company(username, email, password, **company_data):
    """
    Создать учетку юрлица.
    Создать профиль юрлица.
    """
    with transaction.atomic():
        user = get_user_model().company_objects.create_user(
            username=username, email=email, password=password)
        return CompanyProfile.objects.create(user=user, **company_data)


def create_employee(username, email, password, branch_uuid, 
                    position_uuid, **employee_data):
    """
    Создать учетку работника.
    Создать профиль работника.
    """
    branch = Branch.objects.get(uuid=branch_uuid)
    position = Position.objects.get(uuid=position_uuid)
    with transaction.atomic():
        user = get_user_model().employee_objects.create_user(
            username=username, email=email, password=password)
        return EmployeeProfile.objects.create(user=user, branch=branch, 
                                                position=position, **employee_data)


def employee_to_archive(employee_uuid):
    """
    Переводит работника в архив.
    Учетная запись деактивируется.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    user = employee.user
    with transaction.atomic():
        employee.to_archive()
        user.deactivate()
    return employee


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
    return employee


def create_branch(company_uuid, **branch_data):
    """
    Создает филиал.
    """
    company = CompanyProfile.objects.get(uuid=company_uuid)
    return Branch.objects.create(company=company, **branch_data)


def branch_to_archive(branch_uuid, force=False):
    """
    Перевод филиала в архивный статус.
    :param force: Флаг указывающий на принудительное архивирование работников.
    Если не указан и на филиале числятся работники со статусом Работает то будет выброшена ошибка валидации.
    """
    branch = Branch.objects.get(uuid=branch_uuid)
    if not force:
        validators.validate_branch_to_archive(branch)
    with transaction.atomic():
        try:
            for employee in branch.employees.all():
                employee_to_archive(employee.uuid)
        except ObjectDoesNotExist:
            pass
        branch.to_archive()
    return branch


def branch_to_work(branch_uuid):
    """
    Перевод филиала в статус Работает.
    Работники остаются в архиве.
    """
    branch = Branch.objects.get(uuid=branch_uuid)
    validators.validate_branch_to_work(branch)
    branch.to_work()
    return branch


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
    return company


def company_to_work(company_uuid):
    """
    Перевод юрлица в статус Работает.
    Филиалы и работники остаются в архиве.
    Активирование учетной записи
    """
    company = CompanyProfile.objects.get(uuid=company_uuid)
    with transaction.atomic():
        company.to_work()
        company.user.activate()
    return company


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
    branch = Branch.objects.get(uuid=branch_uuid)
    with transaction.atomic():
        try:
            for employee in  branch.employees.all():
                delete_employee(employee.uuid)
        except ObjectDoesNotExist:
            # В филиале нет работников
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
        except ObjectDoesNotExist:
            # у юрлица нет филиалов
            pass
        company.delete()
        user.delete()


def change_employee_position(employee_uuid, new_position_uuid):
    """
    Изменить должность работника.
    """
    employee = EmployeeProfile.objects.get(uuid=employee_uuid)
    new_position = Position.objects.get(uuid=new_position_uuid)
    employee.position = new_position
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


def position_to_archive(position_uuid):
    """
    Переводит должность в архив.
    """
    position = Position.objects.get(uuid=position_uuid)
    position.to_archive()
    return position


def position_to_work(position_uuid):
    """
    Переводит должность в рабочий статус.
    """
    position = Position.objects.get(uuid=position_uuid)
    position.to_work()
    return position