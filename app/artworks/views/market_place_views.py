from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from artworks.serializer import MarketPlaceSerializer
from artworks.models import Artwork, TheMarketPlace
from django.http import HttpResponse
from rest_framework.response import Response
import json
import requests


@api_view(['GET'])
def fetch_market_place(request):
    market_place = TheMarketPlace.objects.first()
    serializer = MarketPlaceSerializer(market_place, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_transaction_fee(request, pk):
    response = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    data = response.json()
    ether_price = data['ethereum']['usd']  # e.g $3950
    market_place = TheMarketPlace.objects.first()
    artwork = Artwork.objects.get(_id=pk)

    market_data = market_place.fetch_transaction_fee(float(artwork.price))
    transaction_fee_dollar = market_data['transaction_fee']
    shipping_price_dollar = market_data['shipping_price']
    artwork_price_dollar = artwork.price

    # e.g ETH 1.5251
    transaction_fee_ether = (
        float(1/(int(data['ethereum']['usd'])) * transaction_fee_dollar))

    # e.g ETH 1.5251
    shipping_price_ether = (
        float(1/(int(data['ethereum']['usd'])) * shipping_price_dollar))

    # e.g ETH 1.5251
    artwork_price_ether = (
        float(1/(int(data['ethereum']['usd'])) * artwork_price_dollar))

    return HttpResponse(json.dumps({
        'ether_price': str(ether_price),
        'shipping_price_ether': str(shipping_price_ether),
        'shipping_price_dollar': int(shipping_price_dollar),
        'artwork_price_ether': str(artwork_price_ether),
        'artwork_price_dollar': int(artwork_price_dollar),
        'transaction_fee_ether': str(transaction_fee_ether),
        'transaction_fee_dollar': int(transaction_fee_dollar),
    }),
        content_type="application/json")


@ api_view(['PUT'])
@ permission_classes([IsAdminUser])
def deploy_market_place(request):
    user = request.user
    data = request.data
    if user:
        marketPlace = TheMarketPlace.objects.create(
            contract=data['marketPlaceAddress'])

    marketPlace.save()
    return HttpResponse(marketPlace.contract)
