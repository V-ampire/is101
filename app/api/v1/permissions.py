from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Доступ только для учетной записи привязанной к запрашиваемому юр. лицу или админов.
        """
        return obj.user == request.user or request.user.is_staff