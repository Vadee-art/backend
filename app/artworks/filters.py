from django_filters import BaseInFilter, CharFilter, NumberFilter
from django_filters import rest_framework as filters

from artworks.models import Artist, Artwork, Origin


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ArtworkFilter(filters.FilterSet):
    price__gt = NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = NumberFilter(field_name="price", lookup_expr="lt")
    origin = NumberInFilter(field_name='artist__origin_id', lookup_expr='in')
    category = NumberInFilter(field_name='category_id', lookup_expr='in')
    sub_category = NumberInFilter(field_name='sub_category_id', lookup_expr='in')

    class Meta:
        model = Artwork
        fields = ["category", "origin", "sub_category"]


class ArtistFilter(filters.FilterSet):
    name_starts = CharFilter(field_name="user__first_name", lookup_expr="istartswith")
    origin = NumberInFilter(field_name='origin_id', lookup_expr='in')

    class Meta:
        model = Artist
        fields = [
            'birthday',
            'origin',
            'achievements',
            'favorites',
        ]


class OriginFilter(filters.FilterSet):
    country = CharFilter(field_name="country", lookup_expr="iexact")

    class Meta:
        model = Origin
        fields = ["country"]
