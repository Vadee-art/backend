from backend.premissions import OwnerPermission
from cart.models import Cart
from cart.serializers import CartSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import permissions, views
from rest_framework.response import Response


class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.available_objects.all()

    def get(self, request):

        cart = get_object_or_404(Cart, user=request.user)
        return Response(data=CartSerializer(cart, context={"request": request}).data)
