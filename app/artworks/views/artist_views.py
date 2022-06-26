from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from artworks.serializer import ArtworkSerializer, ArtistSerializer, TagSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Artist, Artwork, Tag
from rest_framework import filters, generics
from django.db.models import F


class ArtistSearch(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ["^_id"]


#   find artworks with the same category as the artist artworks categories => then find artist of those artworks


class ArtistSmililarArtists(generics.ListAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self, *args, **kwargs):
        artistId = self.kwargs.get("artistId", None)
        artist = Artist.objects.filter(_id=artistId).first()
        artist_artworks_cats = artist.artwork_artist.all().values("category___id")

        list = []
        for c in artist_artworks_cats:
            artworksByArtistCats = Artwork.objects.filter(
                category___id=c["category___id"]
            )
            for a in artworksByArtistCats:
                if a.artist not in list and a.artist != artist:
                    list.append(a.artist)

        return list


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
            artworksByTags = Artwork.objects.filter(tags___id=x["tags___id"]).exclude(
                tags___id=None
            )

            for a in artworksByTags:
                if a not in list:
                    list.append(a)

        return list


@api_view(["GET"])
def artist_list(request):
    query_alphabet = request.query_params.get("alphabet")
    artists = Artist.objects.filter(
        user__last_name__startswith=query_alphabet or ""
    ).all()
    serializer = ArtistSerializer(artists, many=True)
    return Response({"artists": serializer.data})


@api_view(["GET"])
def artist_by_id(request, pk):
    artist = Artist.objects.get(_id=pk)
    artist_artworks = Artwork.objects.filter(artist=artist).order_by("created_at")
    serializerArtist = ArtistSerializer(artist, many=False)
    serializerArtworks = ArtworkSerializer(artist_artworks, many=True)
    return Response(
        {"artist": serializerArtist.data, "artworks": serializerArtworks.data}
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_artist_gallery(request, pk):
    artist = Artist.objects.get(_id=pk)
    data = request.data
    artist.gallery_address = data["galleryAddress"]
    artist.wallet_address = data["artistWalletAddress"]
    artist.save()
    serializer = ArtistSerializer(artist, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def fetch_is_talent(request):
    artist = Artist.objects.filter(is_talent=True).first()
    serializer = ArtistSerializer(artist, many=False)
    return Response(serializer.data)
