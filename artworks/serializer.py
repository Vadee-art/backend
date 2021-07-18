from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Artwork, Order, OrderItem, ShippingAddress, Artist


class ArtistSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
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
    username = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email',
                  'firstName', 'lastName', 'isAdmin']

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
        model = User
        fields = ['id', '_id', 'username', 'email',
                  'firstName', 'lastName', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        # our token is going to be an access token not refresh one
        return str(token.access_token)


class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'


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
