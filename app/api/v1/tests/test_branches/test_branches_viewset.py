from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.factories import CompanyUserAccountModelFactory

from company.factories import BranchFactory
from company.models import Branch

from api.v1.tests.base import BaseViewSetTest

from api.v1.branches import serializers
from api.v1.branches.views import BranchesViewSet

from factory_generator import generate_to_db, generate_to_dict
from faker import Faker
import pytest


fake = Faker()


# @pytest.mark.django_db
# class TestViewSet(BaseViewSetTest):
#     app_name = 'api_v1'
#     url_basename = 'company-branches'
#     factory_class = BranchFactory

#     def setup_method(self, method):
#         super().setup_method(method)
#         self.tested_branch = generate_to_db(BranchFactory)[0]
#         self.permitted_users = self.tested_branch.permitted_users
#         self.permitted_clients = [self.get_api_client(user=user) for user in self.permitted_users]

#     def test_get_queryset(self):
#         request_kwargs = {
#             'company_uuid': self.tested_branch.company.uuid,
#             'uuid': self.tested_branch.uuid
#         }
#         rf = APIRequestFactory()
#         request = rf.get('/branches/')
#         force_authenticate(request, user=self.admin_user)
#         viewset = BranchesViewSet()
#         view = viewset.as_view({'get': 'retrieve'})
#         response = view(request, **request_kwargs)
#         expected_queryset = Branch.objects.filter(company__uuid=self.tested_branch.company.uuid)
#         assert viewset.get_queryset() == expected_queryset
