from artworks.filters import OriginFilter
from artworks.models import (
    Origin,
)
from artworks.serializer import (
    OriginSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets


class OriginViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer
    ordering_fields = ['-_id']
    ordering = ['-_id']
    filter_backends = [DjangoFilterBackend]
    filterset_class = OriginFilter
