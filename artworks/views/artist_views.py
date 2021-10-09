from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from artworks.serializer import ArtworkSerializer, UserSerializer, ArtistSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Artist, Artwork
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchArtistList(request):
    artist = Artist.objects.all()
    serializer = ArtistSerializer(artist, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchArtistArtworks(request, pk):
    artist = Artist.objects.get(_id=pk)
    artworks = Artwork.objects.filter(
        artist=artist).order_by('created_at')
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)
