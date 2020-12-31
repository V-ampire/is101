from rest_framework import permissions

from accounts.models import UserAccount


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
        return request.user.role == UserAccount.COMPANY or request.user.is_staff