from django.contrib.auth import get_user_model
from django.db import transaction

from company.models import Company, Employee, Position, Branch


def delete_company(company_pk):
    """
    Удаление юрлица.
    Вместе с юрлицом удаляется его учетная запись.
    """
    with transaction.atomic():
        company = Company.objects.get(pk=company_pk)
        user = get_user_model().company_objects.get(pk=company.user.pk)
        company.delete()
        user.delete()


def create_company(user_pk, **company_data):
    """
    Создать юрлицо.
    :param user_pk: Primary key учетной записи для юрлица.
    """
    user = get_user_model().company_objects.get(pk=user_pk)
    return Company.objects.create(user=user, **company_data)


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
