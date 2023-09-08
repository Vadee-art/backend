import json

from artworks.filters import ArtworkFilter, OriginFilter
from artworks.models import (
    Artwork,
    Category,
    Order,
    Origin,
    ShippingAddress,
    SubCategory,
    TheToken,
    Voucher,
)
from artworks.serializer import (
    ArtworkSerializer,
    CategorySerializer,
    OrderSerializer,
    OriginSerializer,
    SimpleArtworkSerializer,
    SubCategorySerializer,
    VoucherSerializer,
)
from django.db.models import F, Window
from django.db.models.functions import Rank
from django.http import HttpResponse
from django_cte import With
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


class OriginViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Origin.objects.all()
    serializer_class = OriginSerializer
    ordering_fields = ['-_id']
    ordering = ['-_id']
    filter_backends = [DjangoFilterBackend]
    filterset_class = OriginFilter
