from rest_framework import serializers

from companies.models import Position


class PositionSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для должностей.
    """
    status = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Position
        fields = ('uuid', 'title', 'status')
