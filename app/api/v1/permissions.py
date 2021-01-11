from django.contrib.auth import get_user_model

from rest_framework import permissions

from accounts.utils import is_company_user_account


class IsPermittedOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Доступ только для тех учетных записей которым разрешен доступ или админов.
        Список учетных записей, у которых есть доступ быть определен 
        в аттрибуте allow_users
        """
        try:
            return request.user in obj.permitted_users or request.user.is_staff
        except AttributeError:
            # Отсутствует аттрибут allow_users
            return False


class IsCompanyOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Доступ только у юрлиц и админов.
        """
        return is_company_user_account(request.user) or request.user.is_staff