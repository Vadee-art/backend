from artworks.serializer import ArtworkSerializer
from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    artworks = ArtworkSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
