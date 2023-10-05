from artworks.filters import ArtistFilter
from artworks.models import Achievement, Artist, Artwork, Origin
from artworks.serializer import (
    AchievementSerializer,
    ArtistSerializer,
    ArtworkSerializer,
    OriginSerializer,
    SingleArtistSerializer,
)
from backend.premissions import OwnProfilePermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, views, viewsets
from rest_framework.response import Response


class ArtistSearch(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ["^_id"]


#   find artworks with the same category as the artist artworks categories => then find artist of those artworks


class ArtistSimilarArtists(generics.ListAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self, *args, **kwargs):
        artistId = self.kwargs.get("artistId")
        artist = get_object_or_404(Artist, pk=artistId)
        if artist_artworks_cats := artist.artworks.all().values("category___id"):
            list = []
            for c in artist_artworks_cats:
                artworksByArtistCats = Artwork.objects.filter(category___id=c["category___id"])
                for a in artworksByArtistCats:
                    if a.artist not in list and a.artist != artist and a.artist is not None:
                        list.append(a.artist)

            return list
        else:
            return []


class ArtistRelatedArtworks(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self, *args, **kwargs):
        artistId = self.kwargs.get("artistId", None)
        artist = get_object_or_404(Artist, pk=artistId)
        artist_artworks_tags = artist.artworks.all().values("tags___id")
        artworks_tags = Artwork.objects.all().values("tags___id")
        intersection = artworks_tags.intersection(artist_artworks_tags)
        # intersection = artworks_tags[0].values() & artist_artworks_tags[0].values()
        list = []
        for x in intersection:
            artworksByTags = Artwork.objects.filter(tags___id=x["tags___id"]).exclude(
                tags___id=None
            )

            for a in artworksByTags:
                if a not in list:
                    list.append(a)

        return list


class ArtistsView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtistFilter
    permission_classes = [OwnProfilePermission]
    ordering = ['first_name', 'last_name']
    serializer_classes = {
        'retrieve': SingleArtistSerializer,
    }

    default_serializer_class = ArtistSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        if self.action == 'retrieve':
            return Artist.objects.select_related('origin', 'user').prefetch_related(
                'favorites',
                'achievements',
                'artworks',
                'artworks__collection',
                'artworks__category',
                'artworks__origin',
                'artworks__sub_category',
                'artworks__voucher',
                'artworks__artist__user',
                'artworks__owner',
                'artworks__tags',
            )
        return Artist.objects.select_related('origin', 'user').prefetch_related(
            'favorites',
            'achievements',
        )


class ArtistFiltersView(views.APIView):
    def get(self, request):
        origins = Origin.objects.order_by("_id")
        achievements = Achievement.objects.order_by("_id")

        result = dict(
            origins=OriginSerializer(origins, many=True, context={"request": request}).data,
            achievements=AchievementSerializer(
                achievements, many=True, context={"request": request}
            ).data,
        )
        return Response(data=result)
