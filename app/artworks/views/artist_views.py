from artworks.filters import ArtistFilter
from artworks.models import Achievement, Artist, Artwork, Origin
from artworks.serializer import (
    AchievementSerializer,
    ArtistSerializer,
    ArtworkSerializer,
    OriginSerializer,
    SimpleArtistSerializer,
    SingleArtistSerializer,
)
from backend.premissions import OwnProfilePermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class ArtistSearch(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ["^_id"]


#   find artworks with the same genre as the artist artworks categories => then find artist of those artworks


class ArtistSimilarArtists(views.APIView):
    def get(self, request, id):
        artist = get_object_or_404(
            Artist.objects.get_for_user(request.user),
            pk=id,
        )
        similar_artist = (
            Artist.objects.get_for_user(request.user)
            .filter(
                similar_artists__in=[artist],
            )
            .select_related('origin', 'user')
            .prefetch_related(
                'favorites',
                'achievements',
                'similar_artists',
            )
        )
        result = SimpleArtistSerializer(
            similar_artist, many=True, context={"request": request}
        ).data
        return Response(data=result)


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
    authentication_classes = [JWTAuthentication]
    permission_classes = [OwnProfilePermission]
    ordering = ['first_name', 'last_name']
    serializer_classes = {
        'retrieve': SingleArtistSerializer,
        'list': SimpleArtistSerializer,
    }

    default_serializer_class = ArtistSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        if self.action == 'retrieve':
            return (
                Artist.objects.get_for_user(self.request.user)
                .select_related('origin', 'user')
                .prefetch_related(
                    'favorites',
                    'achievements',
                    'artworks',
                    'similar_artists',
                )
            )

        if self.action == 'list':
            return Artist.objects.get_for_user(self.request.user).select_related('origin', 'user')

        queryset = (
            Artist.objects.get_for_user(self.request.user)
            .select_related('origin', 'user')
            .prefetch_related(
                'favorites',
                'achievements',
                'similar_artists',
            )
        )

        return queryset


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


class FollowArtistView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        artist = get_object_or_404(Artist, pk=id)
        request.user.followed_artists.add(artist)
        request.user.save()
        return Response()


class UnFollowArtistView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        artist = get_object_or_404(Artist, pk=id)
        request.user.followed_artists.remove(artist)
        request.user.save()
        return Response()
