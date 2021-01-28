from django.contrib.auth import get_user_model

from rest_framework import permissions

from accounts.utils import is_company_user_account

from companies.utils import is_company_permitted_user, is_employee_permitted_user

import logging


logger = logging.getLogger(__name__)


class CompanyResourcePermission(permissions.BasePermission):
    """
    Регулирует доступ к вложенным ресурсом юрлица.
    Например, филиалам, работника и т.д.
    """
    def has_permission(self, request, view):
        try:
            company_uuid = view.kwargs['company_uuid']
        except KeyError:
            logger.warning(f"В url ресурса для view {view.basename} отсутсвует аргумент company_uuid")
            return False
        return is_company_permitted_user(company_uuid, request.user.uuid)


class IsPermittedToEmployeeUser(permissions.BasePermission):
    """
    Регулирует доступ к учетной записи работника.
    """
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, employee):
        
        return is_employee_permitted_user(employee.uuid, request.user.uuid)


class IsCompanyOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Доступ только у юрлиц и админов.
        """
        return is_company_user_account(request.user) or request.user.is_staff