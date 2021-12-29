from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from artworks.serializer import ArtistSerializer, ArtworkSerializer, UserSerializer, UserSerializerWithToken
from artworks.models import Artwork, Artist, MyUser
from rest_framework import status

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

#  Customizing token claims with JWT / overriding


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims, meaning when token decrypted more data is available check jwt.io
        token['username'] = user.user_name
        token['message'] = 'hello world'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['username'] = self.user.username
        # data['email'] = self.user.email
        #  ...
        # refactored to the following:
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = MyUser.objects.create(
            first_name=data['firstName'],
            last_name=data['lastName'],
            user_name=data['email'],
            email=data['email'],
            password=make_password(data['password'])

        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail: User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user

    data = request.data
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    if 'checked' in data:
        user.country = data['country']
        user.city = data['city']
        user.province = data['province']
        user.phone_number = data['phoneNumber']
        user.postal_code = data['postalCode']
        user.address = data['address']
    if 'email' in data:
        user.email = data['email']
        user.username = data['email']
    if (('password' in data) and (data['password'] != '')):
        user.password = make_password(data['password'])

    user.save()
    serializer = UserSerializerWithToken(user, many=False)

    return Response(serializer.data)

# since we have wrapped this view with rest-framework decorator and changed the default authentication
# /api/users/profile user is not the same as the user used for /admin


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetchUsers(request):
    users = MyUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetchUsersById(request, pk):
    user = MyUser.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserById(request, pk):
    user = MyUser.objects.get(id=pk)

    data = request.data
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    if 'email' in data:
        user.email = data['email']
        user.username = data['email']
    user.is_staff = data['isAdmin']
    user.save()
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request):
    data = request.data
    selectedUsers = data['selectedUsers']
    for id in selectedUsers:
        userDeleting = MyUser.objects.get(id=id)
        userDeleting.delete()
    return Response('users were deleted')


# remove or add artwork to your favorites
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addFavoriteArtwork(request, pk):
    try:
        artwork = get_object_or_404(Artwork, _id=pk)
        if artwork.favorites.filter(id=request.user.id).exists():
            artwork.favorites.remove(request.user)
        else:
            artwork.favorites.add(request.user)
            message = {'detail: We could not make any changes!'}

        return Response(artwork._id)
    except:
        message = {'detail: We could not make any changes!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchFavoriteArtworkList(request):
    artworks = Artwork.objects.filter(favorites=request.user)
    serializer = ArtworkSerializer(artworks, many=True)
    return Response({'favorites': serializer.data})


# remove or add artists to your favorites
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addFavoriteArtist(request, pk):
    try:
        artist = get_object_or_404(Artist, _id=pk)
        if artist.favorites.filter(id=request.user.id).exists():
            artist.favorites.remove(request.user)
        else:
            artist.favorites.add(request.user)
            message = {'detail: We could not make any changes!'}

        return Response(artist._id)
    except:
        message = {'detail: We could not make any changes!'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchFavoriteArtistList(request):
    artists = Artist.objects.filter(favorites=request.user)
    serializer = ArtistSerializer(artists, many=True)
    return Response({'favorites': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchMyArtworks(request):
    try:
        user = request.user
        artworks = Artwork.objects.filter(owner=user)
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({'my_artworks': serializer.data})

    except:
        message = {'details': 'No Artworks'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


