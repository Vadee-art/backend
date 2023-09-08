from django_filters import CharFilter, NumberFilter
from django_filters import rest_framework as filters

from artworks.models import Artist, Artwork, Origin


class ArtworkFilter(filters.FilterSet):
    price__gt = NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Artwork
        fields = ["category", "origin", "sub_category"]


class ArtistFilter(filters.FilterSet):
    name_starts = CharFilter(field_name="user__first_name", lookup_expr="istartswith")

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
