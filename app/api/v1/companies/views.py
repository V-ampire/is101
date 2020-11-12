from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.v1 import mixins
from api.v1.companies import serializers
from api.v1.companies.permissions import IsOwnerOrAdmin

from company.models import Company


class CompanyViewSet(mixins.ViewSetActionPermissionMixin, viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    """
    queryset = Company.objects.all()
    lookup_field = 'uuid'

    permission_action_classes = {
        "list": [IsAdminUser],
        "retrieve": [IsOwnerOrAdmin],
        "create": [IsAdminUser],
        "update": [IsOwnerOrAdmin],
        "partial_update": [IsOwnerOrAdmin],
        "destroy": [IsAdminUser],
     }

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner

        if self.action == "list":
            return serializers.CompanyListSerializer

        if self.action == "create":
            return serializers.CompanySerializerForAdmin

        if self.action == "update":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner
        
        if self.action == "partial_update":
            if self.request.user.is_staff:
                return serializers.CompanySerializerForAdmin
            return serializers.CompanySerializerForOwner
        

