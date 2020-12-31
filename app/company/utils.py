from django.contrib.auth import get_user_model
from django.db import transaction

from company.models import Company


def delete_company(company_pk):
    """
    Удаление юрлица.
    Вместе с юрлицом удаляется его учетная запись.
    """
    with transaction.atomic():
        company = Company.objects.get(pk=company_pk)
        user = get_user_model().company_objects.get(pk=company.user.pk)
        company.delete()
        user.delete()


def create_company(user_pk, **company_data):
    """
    Создать юрлицо.
    :param user_pk: Primary key учетной записи для юрлица.
    """
    user = get_user_model().company_objects.get(pk=user_pk)
    return Company.objects.create(user=user, **company_data)