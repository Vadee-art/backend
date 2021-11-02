from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from artworks.serializer import ArtworkSerializer, UserSerializer, ArtistSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Artist, Artwork
from rest_framework import status


@api_view(['GET'])
def artist_list(request):
    query_alphabet = request.query_params.get('artist')
    if query_alphabet:
        artists = Artist.objects.filter(text__startswith=query_alphabet).all()
        serializer = ArtistSerializer(artists, many=True)
        return Response({'artists': serializer.data})
    artist = Artist.objects.all()
    serializer = ArtistSerializer(artist, many=True)
    return Response(serializer.data)


@ api_view(['GET'])
def artist_by_id(request, pk):
    artist = Artist.objects.get(_id=pk)
    artworks = Artwork.objects.filter(
        artist=artist).order_by('created_at')
    serializerArtist = ArtistSerializer(artist, many=False)
    serializerArtworks = ArtworkSerializer(artworks, many=True)
    return Response({'details': serializerArtist.data, 'artworks': serializerArtworks.data})
