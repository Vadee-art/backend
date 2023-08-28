from artworks.models import Artwork
from backend.exceptions import ArtworkSoldOut
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, views
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import AddCartItemSerializer, CartSerializer


class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.available_objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @swagger_auto_schema(
        responses = {
            '200' : CartSerializer,
        },
    )
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        return Response(data=CartSerializer(cart, context={"request": request}).data)


    @swagger_auto_schema(
        request_body=AddCartItemSerializer,
        responses = {
            '200' : CartSerializer,
        },
    )
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        data = AddCartItemSerializer(request.data).data
        artwork = get_object_or_404(Artwork, pk=data['artwork_id'])
        if artwork.quantity < 1:
            raise ArtworkSoldOut()

        cart.artworks.add(artwork)
        return Response(data=CartSerializer(cart, context={"request": request}).data)
