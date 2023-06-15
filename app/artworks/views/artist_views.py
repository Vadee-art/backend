from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from backend.pagination import Pagination
from artworks.serializer import ArtworkSerializer, ArtistSerializer, SingleArtistSerializer
from rest_framework.response import Response
from artworks.models import Artist, Artwork
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import filters, generics, viewsets, mixins


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
        artist = Artist.objects.filter(_id=artistId).first()
        if artist.artwork_artist.all().values("category___id"):
            artist_artworks_cats = artist.artwork_artist.all().values("category___id")

            list = []
            for c in artist_artworks_cats:
                artworksByArtistCats = Artwork.objects.filter(category___id=c["category___id"])
                for a in artworksByArtistCats:
                    if a.artist not in list and a.artist != artist and a.artist != None:
                        list.append(a.artist)

            return list
        else:
            return []


class ArtistRelatedArtworks(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self, *args, **kwargs):
        artistId = self.kwargs.get("artistId", None)
        artist = Artist.objects.filter(_id=artistId).first()
        artist_artworks_tags = artist.artwork_artist.all().values("tags___id")
        artworks_tags = Artwork.objects.all().values("tags___id")

        intersection = artworks_tags.intersection(artist_artworks_tags)
        # intersection = artworks_tags[0].values() & artist_artworks_tags[0].values()
        list = []
        for x in intersection:
            artworksByTags = Artwork.objects.filter(tags___id=x["tags___id"]).exclude(tags___id=None)

            for a in artworksByTags:
                if a not in list:
                    list.append(a)

        return list


class ArtistsView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['-user__user_name']
    ordering = ['-user__user_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArtistSerializer
        if self.action == 'retrieve':
            return SingleArtistSerializer
        if self.action == 'update':
            return SingleArtistSerializer
        return ArtistSerializer


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def update_artist_gallery(request, pk):
#     artist = Artist.objects.get(_id=)
#     data = request.data
#     artist.gallery_address = data["galleryAddress"]
#     artist.wallet_address = data["artistWalletAddress"]
#     artist.save()
#     serializer = ArtistSerializer(artist, many=False)
#     return Response(serializer.data)
