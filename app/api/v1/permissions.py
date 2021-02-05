from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch

from rest_framework import permissions
from rest_framework.exceptions import NotFound

from accounts.utils import is_company_user

from companies.utils import has_user_perm_to_company, has_user_perm_to_branch, \
    has_user_perm_to_employee, has_user_perm_to_employee_user
from companies.models import CompanyProfile

import logging


logger = logging.getLogger(__name__)


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_company_user(request.user)


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
        return has_user_perm_to_employee_user(employee_uuid, user_uuid)


class IsPermittedToCompanyProfile(permissions.BasePermission):
    """
    Регулирует доступ к информации о юрлице.
    """
    def has_object_permission(self, request, view, company):
        try:
            user_uuid = request.user.uuid
        except AttributeError:
            logger.warning('У пользователя отсутствует атрибут uuid')
            return False
        return has_user_perm_to_company(company.uuid, user_uuid)


class CompanyNestedPemission(permissions.BasePermission):
    """
    Регулирует доступ для вложенных ресурсов юрлица.
    """
    def get_related_company(self, view):
        """
        Возвращает относящийся к ресурсу CompanyProfile.
        """
        try:
            company_uuid = view.kwargs['company_uuid']
        except KeyError:
            raise NoReverseMatch('Вложенный URL юрлица должен содержать UUID юрлица')

        try:
            return CompanyProfile.objects.get(uuid=company_uuid)
        except CompanyProfile.DoesNotExists:
            raise NotFound('Юрлицо, к которому относится запрашиваемый ресурс не найдено')

    def has_permission(self, request, view):
        company = self.get_related_company(view)
        try:
            user_uuid = request.user.uuid
        except AttributeError:
            logger.warning('У пользователя отсутствует атрибут uuid')
            return False
        return has_user_perm_to_company(company.uuid, user_uuid)


class IsPermittedToBranch(CompanyNestedPemission):
    """
    Регулирует доступ к филиалу.
    Ресурс филиала должен быть вложен в ресурс юрлица, например:
    /companies/<company_uuid>/branches/branch_uuid/
    """
    def has_object_permission(self, request, view, branch):
        try:
            user_uuid = request.user.uuid
        except AttributeError:
            logger.warning('У пользователя отсутствует атрибут uuid')
            return False
        return has_user_perm_to_branch(branch.uuid, user_uuid)


class IsPermittedToEmployeeProfile(CompanyNestedPemission):
    """
    Регулирует доступ к профилю работника.
    Ресурс должен быть вложен в ресурс юрлица, например:
    /companies/<company_uuid>/branches/<branch_uuid>/employees/employee_uuid
    """
    def has_object_permission(self, request, view, employee):
        try:
            user_uuid = request.user.uuid
        except AttributeError:
            logger.warning('У пользователя отсутствует атрибут uuid')
            return False
        return has_user_perm_to_employee(employee.uuid, user_uuid)