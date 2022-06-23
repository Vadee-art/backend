from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from artworks.serializer import ArtworkSerializer, ArtistSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Artist, Artwork
from rest_framework import filters, generics


class ArtistSearch(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ["^_id"]


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
    artworks = Artwork.objects.filter(artist=artist).order_by("created_at")
    serializerArtist = ArtistSerializer(artist, many=False)
    serializerArtworks = ArtworkSerializer(artworks, many=True)
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
