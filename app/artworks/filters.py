from django_filters import BaseInFilter, BooleanFilter, CharFilter, NumberFilter
from django_filters import rest_framework as filters

from artworks.models import Artist, Artwork, Origin


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ArtworkFilter(filters.FilterSet):
    price__gt = NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = NumberFilter(field_name="price", lookup_expr="lt")
    origin = NumberInFilter(field_name='artist__origin_id', lookup_expr='in')
    genre = NumberInFilter(field_name='genre_id', lookup_expr='in')
    theme = NumberInFilter(field_name='theme_id', lookup_expr='in')
    technique = NumberInFilter(field_name='technique_id', lookup_expr='in')

    class Meta:
        model = Artwork
        fields = ["genre", "origin", 'theme', 'technique']


class ArtistFilter(filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)

    name_starts = CharFilter(field_name="user__first_name", lookup_expr="istartswith")
    origin = NumberInFilter(field_name='origin_id', lookup_expr='in')
    is_following = BooleanFilter(method='is_following_filter')

    class Meta:
        model = Artist
        fields = [
            'birthday',
            'origin',
            'achievements',
            'favorites',
        ]

    def is_following_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                queryset = queryset.filter(followers=user.id)
            else:
                queryset = queryset.exclude(followers=user.id)

        return queryset


class OriginFilter(filters.FilterSet):
    country = CharFilter(field_name="country", lookup_expr="iexact")

    class Meta:
        model = Origin
        fields = ["country"]
