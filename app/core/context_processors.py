from django.conf import settings


def api_root(request):
    return {'api_root': settings.API_ROOT}