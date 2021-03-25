from rest_framework.serializers import ValidationError

from core.models import Statuses


def validate_status_param(status: str):
    """
    Проверяет GET параметр запроса status.
    """
    if not status in Statuses:
        raise ValidationError(f'Несущестующий статус {status}')
