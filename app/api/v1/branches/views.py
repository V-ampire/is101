from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1 import mixins
from api.v1.permissions import IsPermittedOrAdmin
from api.v1.branches import serializers
from api.v1.branches.validators import validate_branch_to_archivate

from companies.models import Branch


# class BranchesViewSet(mixins.ViewSetActionPermissionMixin, mixins.StatusViewSetMixin, viewsets.ModelViewSet):
#     """
#     Вьюсет для филиалов.
#     """
#     model_class = Branch
#     queryset = Branch.objects.all()
#     lookup_field = 'uuid'
#     permission_classes = [IsPermittedOrAdmin]

#     permission_action_classes = {
#         'destroy': [IsAdminUser],
#     }

#     http_method_names = ['get', 'post', 'patch', 'delete']

#     def get_queryset(self):
#         return self.queryset.filter(company__uuid=self.kwargs['company_uuid'])

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return serializers.BranchListSerializer
#         return serializers.BranchSerializer
    
#     @action(detail=True, methods=['patch'])
#     def archivate(self, request, *args, **kwargs):
#         """
#         Устанавливает юрлицу архиный статус и отключает учетку.
#         """
#         branch = self.get_object()
#         validate_branch_to_archivate(branch_uuid)
#         branch.archivate()
#         return Response({'status': 'Филиал переведен в архив.'})
