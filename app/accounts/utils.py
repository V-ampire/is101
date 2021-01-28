from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import is_safe_url, urlunquote
from django.utils import timezone

from accounts.models import IPAddress, Roles, UserAccount


def get_next_url(request):
    """
    Return previous URL.
    For example to redirect user back to page where he logged in.
    """
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next) # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = settings.LOGIN_REDIRECT_URL
    return next


def get_client_ip(request):
    """
    Получение IP адреса пользователя из запроса
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def process_ip(ip: str) -> IPAddress:
    """
    Обработать и сохранить IP адрес.
    Возвращает экземпляр accounts.models.IPAddress.
    :param ip: IP адрес.
    """
    try:
        ip_adress = IPAddress.objects.get(ip=ip)
        if ip_adress.is_blocked:
            if ip_adress.unblock_time < timezone.now():
                ip_adress.unblock()
    except IPAddress.DoesNotExist:
        ip_adress = IPAddress.objects.create(ip=ip)
    return ip_adress


def process_attempt(ip: str) -> IPAddress:
    """
    Обработать неудачную попытку входа с IP.
    Если лимит попыток исчерпан то ограничить доступ.
    :param ip: IP адрес.
    """
    attempts_15_minutes_block = settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']
    attempts_24_hours_block = settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']

    ip_address, created = IPAddress.objects.get_or_create(ip=ip)
    ip_address.attempts += 1
    ip_address.save()
    if ip_address.attempts in attempts_15_minutes_block:
        ip_address.block(minutes=15)
    elif ip_address.attempts in attempts_24_hours_block:
        ip_address.block(minutes=24*60)
    elif ip_address.attempts > max(attempts_24_hours_block):
        ip_address.attempts = 1
        ip_address.save()
    return ip_address


def change_password(user_pk, new_password):
    """
    Изменить пароль для пользователя.
    :param user_pk: PK пользователя
    :param new_password: Новый пароль
    """
    user = get_user_model().objects.get(pk=user_pk)
    user.set_password(new_password)
    user.save()


def is_admin_user(user):
    if isinstance(user, UserAccount):
        return user.role == Roles.ADMIN
    return False


def is_company_user(user):
    if isinstance(user, UserAccount):
        return user.role == Roles.COMPANY
    return False


def is_employee_user(user):
    if isinstance(user, UserAccount):
        return user.role == Roles.EMPLOYEE
    return False