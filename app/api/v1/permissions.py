from django.contrib.auth import get_user_model

from rest_framework import permissions

from accounts.utils import is_company_user_account

from companies.utils import has_user_perm_to_company, has_user_perm_to_branch, has_user_perm_to_employee

import logging


logger = logging.getLogger(__name__)


def has_perm_to_employee_user(employee_user_uuid, user_uuid):
    """
    Проверяет имеет ли пользователь доступ к учетной записи работника.
    """
    try:
        employee_user = get_user_model().employee_objects.get(uuid=employee_user_uuid)
    except get_user_model().DoesNotExist:
        logger.warning(f"Учетная запись работника с uuid={employee_user_uuid} не существует.")
        return False
    try:
        profile = employee_user.profile
    except ObjectDoesNotExist:
        logger.warning(f"Учетная запись {employee_user.username} работника создана без заполненого профиля")
        return False
    return has_user_perm_to_employee(profile.uuid, user_uuid)


class IsPermittedToEmployeeUser(permissions.BasePermission):
    """
    Регулирует доступ к учетной записи работника.
    """
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, employee):
        return has_perm_to_employee_user(employee.uuid, request.user.uuid)


class IsPermittedToCompanyProfile(permissions.BasePermission):
    """
    Регулирует доступ к информации о юрлице.
    """
    def has_object_permission(self, request, view, company):
        return has_user_perm_to_company(company.uuid, request.user.uuid)