from rest_framework import viewsets
from rest_framework.response import Response

from api.v1.companies import serializers

from company.models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для юр. лиц.
    """
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    list_serializer_class = serializers.CompanyListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = self.list_serializer_class
        context = self.get_serializer_context()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context=context)
        return Response(serializer.data)
        
        