from django.urls import NoReverseMatch
from django.core.exceptions import ImproperlyConfigured

from rest_framework import permissions
from rest_framework.exceptions import NotFound

from accounts.utils import is_company_user, get_employee_user_profile

from companies.models import CompanyProfile


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_company_user(request.user)


class IsCompanyOwnerOrAdmin():
    """
    Доступ для юрлица-владельца и админов.
    Реализует метод get_related_company(self, view) - возвращающий юрлицо.
    URL юрлица должен содержать UUID юрлица, например:
    /companies/<company_uuid_kwarg>/branches/

    View должна содержать атрибут company_uuid_kwarg - имя аргумента содержащего uuid юрлица.
    """
    def get_related_company(self, view):
        """
        Возвращает относящийся к ресурсу CompanyProfile.
        """
        try:
            company_uuid_kwarg = view.company_uuid_kwarg
        except AttributeError:
            raise ImproperlyConfigured('View должна содержать атрибут company_uuid_kwarg - имя аргумента содержащего uuid юрлица.')
        
        try:
            company_uuid = view.kwargs[company_uuid_kwarg]
        except KeyError:
            raise NoReverseMatch('Вложенный URL юрлица должен содержать UUID юрлица')

        try:
            return CompanyProfile.objects.get(uuid=company_uuid)
        except CompanyProfile.DoesNotExist:
            raise NotFound('Юрлицо, к которому относится запрашиваемый ресурс не найдено')
    
    def has_permission(self, request, view):
        """
        Разрешает доступ юрлицу-владельцу и админам.
        """
        company = self.get_related_company(view)
        return company.user == request.user or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


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