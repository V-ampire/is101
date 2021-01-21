from django.contrib.auth import get_user_model
from django.db import transaction

from company.models import Company, Employee, Position, Branch


def delete_company(company_uuid):
    """
    Удаление юрлица.
    Вместе с юрлицом удаляется его учетная запись.
    """
    with transaction.atomic():
        company = Company.objects.get(uuid=company_uuid)
        user = company.user
        company.delete()
        user.delete()


def archivate_company(company_uuid):
    """
    Перевод юрлица в архивный статус.
    Одновременно деактивирует учетную запись.
    """
    with transaction.atomic():
        company = Company.objects.get(uuid=company_uuid)
        user = company.user
        company.archivate()
        user.deactivate()


def activate_company(company_uuid):
    """
    Перевод юрлица в активный статус.
    Одновременно ативирует учетную запись.
    """
    with transaction.atomic():
        company = Company.objects.get(uuid=company_uuid)
        user = company.user
        company.activate()
        user.activate()


def create_company(user_uuid, **company_data):
    """
    Создать юрлицо.
    """
    user = get_user_model().company_objects.get(uuid=user_uuid)
    return Company.objects.create(user=user, **company_data)


def create_employee(user_uuid, **employee_data):
    """
    Создать профиль работника.
    Активировать учетку работника.
    """
    user = get_user_model().employee_objects.get(uuid=user_uuid)
    return Employee.objects.create(user=user, **employee_data)


def change_employee_position(employee_uuid, new_position_uuid):
    """
    Изменить должность работника.
    """
    employee = Employee.objects.get(uuid=employee_uuid)
    new_position = Position.objects.get(uuid=new_position_uuid)
    employee.employee_position = new_position
    employee.save()
    return employee


def transfer_employee_to_branch(employee_uuid, branch_uuid):
    """
    Переводит работника в указанный филиал.
    """
    employee = Employee.objects.get(uuid=employee_uuid)
    new_branch = Branch.objects.get(uuid=branch_uuid)
    employee.branch = new_branch
    employee.save()
    return employee
