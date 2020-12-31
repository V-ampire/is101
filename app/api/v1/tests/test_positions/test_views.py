from django.urls import reverse

from company.factories import PositionFactory
from company.models import Position

from api.v1.positions.serializers import PositionSerializer

import pytest


@pytest.mark.django_db
def test_get_position_list_by_company(api_client, company_user):
    """
    Тест на получение списка юрлицом.
    Юрлицо имеет доступ только к списку активных должностей.
    """
    active_positions = [PositionFactory(status=Position.ACTIVE) for i in range(3)]
    archive_positions = [PositionFactory(status=Position.ARCHIVED) for i in range(3)]
    url = reverse('api_v1:position-list')
    api_client.force_authenticate(user=company_user)
    response = api_client.get(url)

    expected_data = PositionSerializer(
        Position.objects.filter(status=Position.ACTIVE), 
        many=True, 
        context={'request': response.wsgi_request}
    ).data
    assert expected_data == response.json()
