from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from artworks.serializer import ArtworkSerializer, UserSerializer, ArtistSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Artist
from rest_framework import status


@api_view(['GET'])
def fetchArtist(request, pk):
    artist = Artist.objects.get(_id=pk)
    serializer = ArtistSerializer(artist, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetchArtists(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)
