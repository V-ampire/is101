from django.urls import NoReverseMatch

from rest_framework import permissions
from rest_framework.exceptions import NotFound

from accounts.utils import is_company_user, get_employee_user_profile

from companies.models import CompanyProfile


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_company_user(request.user)


class CompanyNestedMixin():
    """
    Миксин для вложенных ресурсов юрлица.
    Реализует метод get_related_company(self, view) - возвращающий юрлицо.
    URL юрлица должен содержать UUID юрлица, например:
    /companies/<company_uuid>/branches/
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


class IsCompanyOwnerOrAdmin(CompanyNestedMixin, permissions.BasePermission):
    """
    Разрешает доступ юрлицу-владельцу и админам.
    """
    def has_permission(self, request, view):
        company = self.get_related_company(view)
        return company.user == request.user or request.user.is_staff


class IsOwnerOrSuperuser(permissions.IsAuthenticated):
    """
    Доступ имеют суперпользователи и владельцы.
    Пользователь должен быть аутентифицирован.
    """
    def has_object_permission(self, request, view, user):
        return request.user == user or request.user.is_superuser


class IsOwnerOrAdmin(permissions.IsAuthenticated):
    """
    Доступ имеют админы и владельцы.
    Пользователь должен быть аутентифицирован.
    """
    def has_object_permission(self, request, view, user):
        return user == request.user or request.user.is_staff


class IsPermittedToEmployeeUser(permissions.IsAuthenticated):
    """
    Регулирует доступ к учетной записи работника.
    Пользователь должен быть аутентифицирован.
    """     
    def has_object_permission(self, request, view, employee_user):
        employee = get_employee_user_profile(employee_user)
        return employee.branch.company.user == request.user or request.user.is_staff