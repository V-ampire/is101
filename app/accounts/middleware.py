from django.conf import settings

from accounts.utils import get_user_uuid


def user_uuid_cookie_middleware(get_response):
    """
    Устанавливает куки user_uuid содержащие UUID пользователя.
    """
    def middleware(request):
        response = get_response(request)
        user_uuid = get_user_uuid(request.user)
        if user_uuid:
            response.set_cookie(settings.USER_UUID_COOKIE_NAME, user_uuid)
        return response
    return middleware