from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from accounts.views import BruteForceLoginView

import pytest


# @pytest.mark.django_db
# # def test_brute_force_login_view_block_for_15_min(rf, mocker):
#     request = rf.post()

@pytest.mark.django_db
class TestBruteForceView():

    @classmethod
    def setup_class(cls, mocker):
        cls.now = timezone.now()
        mock_now = mocker.patch('accounts.models.timezone.now')
        mock_now.return_value = cls.now

    def test(self):
        from accounts.models import timezone as models_timezone
        import time; time.sleep(3)
        print(self.now, models_timezone.now())