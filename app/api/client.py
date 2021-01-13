from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from company.models import Position

p = Position.objects.all()[0]

superuser = get_user_model().objects.filter(is_superuser=True)[0]

api = APIClient()

api.force_authenticate(user=superuser)

url = 'http://127.0.0.1:8000/api/v1/companies/e4925b03-af44-4a1d-9dfa-6968801a4279/branches/2d798e55-5664-41fe-abcb-66938208f06f/employees/16a87f3e-9acc-466d-aef4-ca98f7ee9c60/change_position/'

data = {'uuid': p.uuid}