from rest_framework.decorators import action
from rest_framework.response import Response


class ViewSetActionPermissionMixin:
    
    def get_permissions(self):
        """Return the permission classes based on action.

        Look for permission classes in a dict mapping action to
        permission classes array, ie.:

        class MyViewSet(ViewSetActionPermissionMixin, ViewSet):
            ...
            permission_classes = [AllowAny]
            permission_action_classes = {
                'list': [IsAuthenticated]
                'create': [IsAdminUser]
                'my_action': [MyCustomPermission]
            }

            @action(...)
            def my_action:
                ...

        If there is no action in the dict mapping, then the default
        permission_classes is returned. If a custom action has its
        permission_classes defined in the action decorator, then that
        supercedes the value defined in the dict mapping.

        Refer to https://stackoverflow.com/a/35987077/1677041
        """
        try:
            return [
                permission()
                for permission in self.permission_action_classes[self.action]
            ]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, "kwargs", {})
                permission_classes = action_func_kwargs.get(
                    "permission_classes"
                )
            else:
                permission_classes = None

            return [
                permission()
                for permission in (
                    permission_classes or self.permission_classes
                )
            ]


class StatusViewSetMixin:
    """
    Миксин определяющий действия по изменению статусов объекта,
    определенных в company.models.StatusModel
    """
    @action(detail=True)
    def archivate(self, request, *args, **kwargs):
        """
        Устанавливает объекту статус ARCHIVED.
        Метод GET.
        """
        obj = self.get_object()
        obj.archivate()
        return Response({'status': 'ok'})

    @action(detail=True)
    def activate(self, request, *args, **kwargs):
        """
        Устанавливает объекту статус ACTIVE.
        Метод GET.
        """
        obj = self.get_object()
        obj.activate()
        return Response({'status': 'ok'})