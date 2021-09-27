from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser, Artwork, Order, OrderItem, ShippingAddress, Artist, Category, SubCategory, Tag


class ArtistSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', '_id', 'firstName', 'lastName', 'isAdmin']

    # for changing id to _id and keeping the same convention
    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_username(self, obj):
        return obj.email

    def get_firstName(self, obj):
        return obj.first_name

    def get_lastName(self, obj):
        return obj.last_name


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    phoneNumber = serializers.SerializerMethodField(read_only=True)
    postalCode = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', '_id', 'username', 'email',
                  'firstName', 'lastName', 'country', 'city', 'phoneNumber', 'postalCode', 'address', 'isAdmin']

    # for changing id to _id and keeping the same convention
    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_username(self, obj):
        return obj.email

    def get_firstName(self, obj):
        return obj.first_name

    def get_lastName(self, obj):
        return obj.last_name

    def get_country(self, obj):
        return obj.country

    def get_city(self, obj):
        return obj.city

    def get_phoneNumber(self, obj):
        return obj.phone_number

    def get_postalCode(self, obj):
        return obj.postal_code

    def get_address(self, obj):
        return obj.address


class ArtistSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)
    userId = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artist
        fields = ['userId', '_id', 'username',
                  'firstName', 'lastName']

    def get_userId(self, obj):
        user = obj.user
        userId = user.id
        return userId

    def get_username(self, obj):
        user = obj.user
        email = user.email
        return email

    def get_firstName(self, obj):
        user = obj.user
        firstName = user.first_name
        return firstName

    def get_lastName(self, obj):
        user = obj.user
        lastName = user.last_name
        return lastName


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyUser
        fields = ['id', '_id', 'username', 'email',
                  'firstName', 'lastName', 'isAdmin', 'token']

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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArtworkSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    artist = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Artwork
        fields = '__all__'

    # reverse query set
    def get_user(self, obj):
        user = obj.created_by
        serializer = UserSerializer(user, many=False)
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


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        # reverse query set
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_users(self, obj):
        users = obj.user_set.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            # one to one relation -> obj.shippingAddress
            shippingAddress = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            shippingAddress = False
        return shippingAddress

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)

        return serializer.data
