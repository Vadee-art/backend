from artworks.models import Artist, Artwork, MyUser
from artworks.serializer import (
    ArtistSerializer,
    ArtworkSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileImageSerializer,
    UserSerializerInput,
    UserSerializerOutput,
    Web3TokenObtainPairSerializer,
)
from backend.premissions import UserProfilePermission
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class Web3TokenObtainPairView(TokenObtainPairView):
    serializer_class = Web3TokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserProfile(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = MyUser.objects.filter(is_active=True).select_related(
        'city',
        'city__region',
        'city__country',
    )
    permission_classes = (IsAuthenticated, UserProfilePermission)
    serializer_class = UserSerializerOutput

    @swagger_auto_schema(
        request_body=UserSerializerInput,
        responses={
            status.HTTP_200_OK: UserSerializerOutput,
        },
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerInput
        super().partial_update(request, *args, **kwargs)
        return Response(UserSerializerOutput(self.get_object(), context={"request": request}).data)

    @swagger_auto_schema(
        request_body=UserSerializerInput,
        responses={
            status.HTTP_200_OK: UserSerializerOutput,
        },
    )
    def update(self, request, *args, **kwargs):
        self.serializer_class = UserSerializerInput
        super().update(request, *args, **kwargs)
        return Response(UserSerializerOutput(self.get_object(), context={"request": request}).data)


class UserProfileImage(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = MyUser.objects.filter(is_active=True)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, UserProfilePermission)
    serializer_class = UserProfileImageSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def fetchUsers(request):
    users = MyUser.objects.all()
    serializer = UserSerializerOutput(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def fetchUsersById(request, pk):
    user = MyUser.objects.get(id=pk)
    serializer = UserSerializerOutput(user, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteUser(request):
    data = request.data
    selectedUsers = data["selectedUsers"]
    for id in selectedUsers:
        userDeleting = MyUser.objects.get(id=id)
        userDeleting.delete()
    return Response("users were deleted")


# remove or add artwork to your favorites
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def addFavoriteArtwork(request, pk):
    try:
        artwork = get_object_or_404(Artwork, _id=pk)
        if artwork.favorite_artworks.filter(id=request.user.id).exists():
            artwork.favorite_artworks.remove(request.user)
        else:
            artwork.favorite_artworks.add(request.user)
            message = {"detail: We could not make any changes!"}

        return Response(artwork._id)
    except:
        message = {"detail: We could not make any changes!"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetchFavoriteArtworkList(request):
    artworks = Artwork.objects.filter(favorite_artworks=request.user)
    serializer = ArtworkSerializer(artworks, many=True)
    return Response({"favorites": serializer.data})


# remove or add artists to your favorites
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def addFavoriteArtist(request, pk):
    try:
        artist = get_object_or_404(Artist, _id=pk)
        if artist.favorites.filter(id=request.user.id).exists():
            artist.favorites.remove(request.user)
        else:
            artist.favorites.add(request.user)
            message = {"detail: We could not make any changes!"}

        return Response(artist._id)
    except:
        message = {"detail: We could not make any changes!"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetchFavoriteArtistList(request):
    artists = Artist.objects.get_for_user(request.user).filter(favorites=request.user)
    serializer = ArtistSerializer(artists, many=True)
    return Response({"favorites": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetchMyArtworks(request):
    try:
        user = request.user
        artworks = Artwork.objects.filter(owner=user)
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({"my_artworks": serializer.data})

    except:
        message = {"details": "No Artworks"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
