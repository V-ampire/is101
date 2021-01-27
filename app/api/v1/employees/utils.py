from django.db import transaction
from django.contrib.auth import get_user_model

from company.models import Employee


def create_employee(user_data, employee_data):
    """
    Создать учетную запись и профиль работника.
    :param user_data: Данные учеьной записи.
    :param employee_data: Данные о работнике.
    """
    with transaction.atomic():
        user = get_user_model.employee_objects.create_account(**user_data)
        return Employee.objects.create(user=user, **employee_data)