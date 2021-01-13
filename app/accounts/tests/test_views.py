from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.test import RequestFactory

from accounts.views import BruteForceLoginView
from accounts.models import IPAddress

from faker import Faker
import pytest


fake = Faker()

attempts_15_minutes_block = settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']
attempts_24_hours_block = settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']


@pytest.mark.django_db
class TestBruteForceView():

    @classmethod
    def setup_class(cls):
        cls.now = timezone.now()
        cls.rf = RequestFactory()

    def test_brute_force_login_view_block_for_15_min(self, mocker):
        mock_now = mocker.patch('accounts.models.timezone.now')
        mock_now = self.now
        tested_ip = fake.ipv4()
        invalid_data = {
            'username': fake.user_name(),
            'password': fake.password(),
        }
        request = self.rf.post('/accounts/login', data=invalid_data)
        request.META['REMOTE_ADDR'] = tested_ip
        view = method_decorator(csrf_exempt, name='dispatch')(BruteForceLoginView)
        for attempt in range(attempts_15_minutes_block[0]):
            response = view.as_view()(request)
        result_ip = IPAddress.objects.get(ip=tested_ip)


