from artworks.models import Artwork
from django_filters import NumberFilter
from django_filters import rest_framework as filters


class ArtworkFilter(filters.FilterSet):
    price__gt = NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Artwork
        fields = [
            "category",
            "origin",
            "sub_category"
        ]
