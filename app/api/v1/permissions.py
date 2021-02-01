from django.contrib.auth import get_user_model

from rest_framework import permissions

from companies.utils import has_user_perm_to_company, has_user_perm_to_branch, \
    has_user_perm_to_employee, has_perm_to_employee_user

import logging


logger = logging.getLogger(__name__)


class IsPermittedToEmployeeUser(permissions.BasePermission):
    """
    Регулирует доступ к учетной записи работника.
    """     
    def has_object_permission(self, request, view, employee):
        try:
            employee_uuid = employee.uuid
            user_uuid = request.user.uuid
        except AttributeError:
            logger.warning('У пользователя отсутствует атрибут uuid')
            return False
        return has_perm_to_employee_user(employee_uuid, user_uuid)


class IsPermittedToCompanyProfile(permissions.BasePermission):
    """
    Регулирует доступ к информации о юрлице.
    """
    def has_object_permission(self, request, view, company):
        return has_user_perm_to_company(company.uuid, request.user.uuid)