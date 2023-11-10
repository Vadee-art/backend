from cities_light.contrib.restframework3 import (
    CitySerializer,
    CountrySerializer,
    RegionSerializer,
)
from cities_light.models import City
from django.contrib.auth import authenticate
from eth_account.messages import encode_defunct
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from web3 import Web3

from artworks.validators import validate_password

from .models import (
    Achievement,
    Article,
    Artist,
    Artwork,
    Collection,
    Genre,
    MyUser,
    Order,
    Origin,
    ShippingAddress,
    Tag,
    Technique,
    TheMarketPlace,
    Theme,
    TheToken,
    Voucher,
)


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheMarketPlace
        fields = '__all__'


class UserSerializerInput(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)

    class Meta:
        model = MyUser
        exclude = (
            'is_staff',
            'is_admin',
            'is_active',
            'is_superuser',
            'user_permissions',
            'groups',
        )
        extra_kwargs = {
            'password': {'required': False, 'write_only': True},
            'email': {'required': True},
            'user_name': {'required': False},
            'last_login': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, data):
        super().validate(data)
        if 'password' in data:
            validate_password(data['password'], data)
        return data


class UserSerializerOutput(serializers.ModelSerializer):
    city = CitySerializer(required=False)
    region = RegionSerializer(read_only=True, required=False, source='city.region')
    country = CountrySerializer(read_only=True, required=False, source='city.country')

    class Meta(UserSerializerInput.Meta):
        pass

    def get_region(self, obj):
        if not obj.city:
            return None
        return RegionSerializer(obj.city.region, context=self.context).data

    def get_country(self, obj):
        if not obj.city:
            return None
        return CountrySerializer(obj.city.country, context=self.context).data


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('profile_picture',)
        extra_kwargs = {
            'profile_picture': {'read_only': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'user_name', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'user_name': {'required': True, 'allow_blank': False},
        }

    def create(self, data):
        user = MyUser.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_name=data['user_name'],
            email=data['email'],
        )

        validate_password(data['password'], user)
        user.set_password(data['password'])
        user.save()
        return user


class UserSerializerWithToken(UserSerializerOutput):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'isAdmin',
            'token',
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        # our token is going to be an access token not refresh one
        return str(token.access_token)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class TechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technique
        fields = '__all__'


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = '__all__'


class OriginWithArtworksSerializer(OriginSerializer):
    artworks = serializers.SerializerMethodField(read_only=True)

    def get_artworks(self, obj):
        return SimpleArtworkSerializer(obj.artworks, many=True, context=self.context).data

    class Meta:
        model = Origin
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    token_uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Voucher
        fields = '__all__'

    def get_token_uri(self, obj):
        return obj.token_uri


class TheTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheToken
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    origin = OriginSerializer(many=False, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        read_only_fields = [
            "user",
            "origin",
            "achievements",
            "favorites",
            "contract",
            "vadee_fee",
        ]
        exclude = ["gallery_address"]

    def get_username(self, obj):
        return obj.user.email

    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_is_following(self, obj):
        return obj.followers.filter(id=self.context['request'].user.id).exists()


class SimpleArtistSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    origin = OriginSerializer(many=False, read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        fields = ('_id', 'name', 'origin', 'photo', 'is_following')

    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_is_following(self, obj):
        return obj.followers.filter(id=self.context['request'].user.id).exists()


class ArtworkSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    collection = CollectionSerializer(read_only=True, many=False)
    artist = ArtistSerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=False, read_only=True)
    voucher = VoucherSerializer(many=False, read_only=True)
    image_medium_quality = serializers.SerializerMethodField(read_only=True)
    theme = ThemeSerializer(many=False, read_only=True)
    technique = TechniqueSerializer(many=False, read_only=True)

    class Meta:
        model = Artwork
        fields = '__all__'

    def get_image_medium_quality(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_medium_quality.url)


class ArtworkWithoutArtistSerializer(ArtworkSerializer):
    artist = None

    class Meta:
        model = Artwork
        exclude = ('artist',)


class SimpleArtworkSerializer(serializers.ModelSerializer):
    image_medium_quality = serializers.SerializerMethodField(read_only=True)
    artist = SimpleArtistSerializer(many=False, read_only=True)

    class Meta:
        model = Artwork
        fields = ('_id', 'price', 'image', 'title', 'artist', 'image_medium_quality')

    def get_image_medium_quality(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_medium_quality.url)


class CarouselSerializer(serializers.ModelSerializer):
    collection = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = ("title", "artist_name", "collection", "image")

    def get_collection(self, obj):
        collection = obj.collection
        serializer = CollectionSerializer(collection, many=False)
        return serializer.data

    def get_artist_name(self, obj):
        return obj.artist.user.first_name + obj.artist.user.last_name


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'

    def get_transaction_hash(self, obj):
        transaction_hash = obj.transaction_hash
        serializer = OrderSerializer(transaction_hash, many=False)
        return serializer.data

    def get_create_at(self, obj):
        artist = obj.artist
        serializer = ArtistSerializer(artist, many=False)
        return serializer.data

    class Meta:
        model = Order
        fields = '__all__'

    def get_shippingAddress(self, obj):
        try:
            # one to one relation -> obj.shippingAddress
            shippingAddress = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            shippingAddress = False
        return shippingAddress

        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class SingleArtistSerializer(ArtistSerializer):
    artworks = ArtworkWithoutArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        token["username"] = user.user_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerOutput(self.user).data
        data['user'] = dict()
        for k, v in serializer.items():
            data['user'][k] = v

        return data


class Web3TokenObtainPairSerializer(serializers.Serializer):
    token_class = RefreshToken

    msg = serializers.CharField(max_length=128, required=True)
    sig = serializers.CharField(max_length=256, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

    def validate(self, attrs):
        msg = attrs['msg']
        sig = attrs['sig']
        signable_msg = encode_defunct(text=msg)

        web3 = Web3()

        try:
            address = web3.eth.account.recover_message(signable_msg, signature=sig)
        except:
            raise serializers.ValidationError(detail='Invalid signature')

        self.user = authenticate(address)
        refresh = self.get_token(self.user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['user'] = UserSerializerOutput(self.user).data
        return data
