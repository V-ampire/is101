from django.conf import settings
from django.utils import timezone

from accounts.models import IPAddress
from accounts import utils
from accounts.facories import BlockedIPAddressFactory, NotBlockedIPAddressFactory

from datetime import timedelta
from faker import Faker
import pytest


tzinfo = timezone.get_current_timezone()

fake = Faker()

@pytest.mark.django_db
def test_process_ip_blocked():
    blocked_ip = BlockedIPAddressFactory()
    expired_blocked_ip = BlockedIPAddressFactory(unblock_time=fake.date_time_this_month(tzinfo=tzinfo))
    expected_blocked = utils.process_ip(blocked_ip.ip)
    expected_unblocked = utils.process_ip(expired_blocked_ip.ip)
    assert expected_blocked.is_blocked
    assert not expected_unblocked.is_blocked


@pytest.mark.django_db
def test_process_ip_not_blocked():
    expected_ip = NotBlockedIPAddressFactory()
    result_ip = utils.process_ip(expected_ip.ip)
    assert expected_ip == result_ip


@pytest.mark.django_db
def test_process_ip_not_exist():
    ip = fake.ipv4()
    result_ip = utils.process_ip(ip)
    assert IPAddress.objects.filter(ip=ip).exists()


@pytest.mark.django_db
def test_process_attempt_for_15_min(mocker):
    expected_now = timezone.now()
    mock_now = mocker.patch('accounts.models.timezone.now')
    mock_now.return_value = expected_now
    for attempts_num in settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']:
        ip_address = NotBlockedIPAddressFactory(attempts=attempts_num-1)
        tested_ip_address = utils.process_attempt(ip_address.ip)
        assert tested_ip_address.is_blocked
        assert tested_ip_address.unblock_time == expected_now + timedelta(minutes=15)


@pytest.mark.django_db
def test_process_attempt_for_24_hours(mocker):
    expected_now = timezone.now()
    mock_now = mocker.patch('accounts.models.timezone.now')
    mock_now.return_value = expected_now
    for attempts_num in settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']:
        ip_address = NotBlockedIPAddressFactory(attempts=attempts_num-1)
        tested_ip_address = utils.process_attempt(ip_address.ip)
        assert tested_ip_address.is_blocked
        assert tested_ip_address.unblock_time == expected_now + timedelta(minutes=24*60)


@pytest.mark.django_db
def test_process_attempt_reload_attempts(mocker):
    expected_now = timezone.now()
    mock_now = mocker.patch('accounts.models.timezone.now')
    mock_now.return_value = expected_now
    attempts = max(settings.AUTH_ATTEMPTS['24_HOURS_BLOCK'])
    ip_address = NotBlockedIPAddressFactory(attempts=max(settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']))
    tested_ip_address = utils.process_attempt(ip_address.ip)
    assert not tested_ip_address.is_blocked
    assert tested_ip_address.attempts == 1


@pytest.mark.django_db
def test_process_attempt_for_new_ip():
    ip = fake.ipv4()
    tested_ip_address = utils.process_attempt(ip)
    assert tested_ip_address.attempts == 1