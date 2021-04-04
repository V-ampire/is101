from django.conf import settings

from accounts import utils


def user_uuid_cookie_middleware(get_response):
    """
    Устанавливает куки user_uuid содержащие UUID пользователя.
    """
    def middleware(request):
        response = get_response(request)
        user_uuid = utils.get_user_uuid(request.user)
        if user_uuid:
            response.set_cookie(settings.USER_UUID_COOKIE_NAME, user_uuid, samesite='Strict')
        return response
    return middleware


def user_profile_uuid_cookie_middleware(get_response):
    """
    Устанавливает куки с uuid работника или юрлица.
    """
    def middleware(request):
        response = get_response(request)
        profile = None
        if utils.is_company_user(request.user):
            profile = utils.get_company_user_profile(request.user)
        elif utils.is_employee_user(request.user):
            profile = utils.get_employee_user_profile(request.user)
        
        if profile:
            response.set_cookie(settings.PROFILE_UUID_COOKIE_NAME, profile.uuid, samesite='Strict')
        return response
    return middleware