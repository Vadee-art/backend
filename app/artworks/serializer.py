from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Article,
    MyUser,
    Artwork,
    Order,
    Origin,
    ShippingAddress,
    Artist,
    Category,
    TheMarketPlace,
    TheToken,
    Voucher,
    SubCategory,
    Tag,
    Achievement,
    Collection,
)


class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheMarketPlace
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    province = serializers.SerializerMethodField(read_only=True)
    phoneNumber = serializers.SerializerMethodField(read_only=True)
    postalCode = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    wallet_address = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    artist = serializers.SerializerMethodField(read_only=True)
    # id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    # favorite_artworks = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = [
            'id',
            'artist',
            'username',
            'email',
            'first_name',
            'last_name',
            'country',
            'city',
            'province',
            'phoneNumber',
            'postalCode',
            'address',
            'isAdmin',
            'wallet_address',
            'password'
            # 'favorite_artworks',
        ]

    # for changing id to _id and keeping the same convention
    # def get_id(self, obj):
    #     return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_username(self, obj):
        return obj.email

    def get_first_name(self, obj):
        return obj.first_name

    def get_last_name(self, obj):
        return obj.last_name

    def get_country(self, obj):
        return obj.country

    def get_city(self, obj):
        return obj.city

    def get_province(self, obj):
        return obj.province

    def get_phoneNumber(self, obj):
        return obj.phone_number

    def get_postalCode(self, obj):
        return obj.postal_code

    def get_address(self, obj):
        return obj.address

    def get_wallet_address(self, obj):
        return obj.wallet_address

    # def get_favorite_artworks(self, obj):
    #     artworks = obj.user_favorite_artworks
    #     serializer = ArtworkSerializer(artworks, many=True)
    #     return serializer.data

    def get_artist(self, obj):
        artist = getattr(obj, 'artist', None)
        if artist is None:
            return None
        if artist:
            serializer = ArtistSerializer(artist, many=False)
            return serializer.data


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
        user.set_password(data['password'])
        user.save()
        return user


class UserSerializerWithToken(UserSerializer):
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


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    # reverse query set
    def get_sub_categories(self, obj):
        subCategories = obj.subcategory_set.all()
        serializer = SubCategorySerializer(subCategories, many=True)
        return serializer.data


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'


class TheTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheToken
        fields = '__all__'


class ArtistArtworksSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    artwork_artist = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

    def get_artwork_artist(self, obj):
        artworks = obj.artwork_artist
        serializer = ArtworkSerializer(artworks, many=True)
        return obj.artwork_artist


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    userId = serializers.SerializerMethodField(read_only=True)
    origin = serializers.SerializerMethodField(read_only=True)
    achievements = serializers.SerializerMethodField(read_only=True)
    gallery_address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

    def get_userId(self, obj):
        user = obj.user
        userId = user.id
        return userId

    def get_first_name(self, obj):
        user = obj.user
        return user.first_name

    def get_last_name(self, obj):
        user = obj.user
        return user.last_name

    def get_photo(self, obj):
        return obj.photo.url

    def get_origin_country(self, obj):
        return obj.origin.country

    def get_origin(self, obj):
        origin = obj.origin
        serializer = OriginSerializer(origin, many=False)
        return serializer.data

    def get_achievements(self, obj):
        achievements = obj.achievements
        serializer = AchievementsSerializer(achievements, many=True)
        return serializer.data

    def get_gallery_address(self, obj):
        return obj.gallery_address


class ArtworkSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    collection = serializers.SerializerMethodField(read_only=True)
    artist = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)
    origin = serializers.SerializerMethodField(read_only=True)
    voucher = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artwork
        fields = '__all__'

    def get_user(self, obj):
        user = obj.created_by
        serializer = UserSerializer(user, many=False)
        return serializer.data

    def get_collection(self, obj):
        collection = obj.collection
        serializer = CollectionSerializer(collection, many=False)
        return serializer.data

    def get_artist(self, obj):
        artist = obj.artist
        serializer = ArtistSerializer(artist, many=False)
        return serializer.data

    def get_tags(self, obj):
        tags = obj.tags
        serializer = TagSerializer(tags, many=True)
        return serializer.data

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data

    def get_sub_category(self, obj):
        sub_category = obj.sub_category
        serializer = SubCategorySerializer(sub_category, many=False)
        return serializer.data

    def get_origin(self, obj):
        origin = obj.origin
        serializer = OriginSerializer(origin, many=False)
        return serializer.data

    def get_voucher(self, obj):
        voucher = obj.voucher
        serializer = VoucherSerializer(voucher, many=False)
        return serializer.data


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
