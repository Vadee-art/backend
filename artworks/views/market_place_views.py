from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from artworks.serializer import MarketPlaceSerializer
from artworks.models import TheMarketPlace
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
def fetch_transaction_fee(request, price):
    response = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    data = response.json()
    ether_price = data['ethereum']['usd']  # e.g $3950
    market_place = TheMarketPlace.objects.first()

    transaction_fee_dollar = market_place.fetch_transaction_fee(float(price))

    # e.g ETH 1.5251
    transaction_fee_ether = (
        float(1/(int(data['ethereum']['usd'])) * transaction_fee_dollar))

    return HttpResponse(json.dumps({
        'ether_price': str(ether_price),
        'transaction_fee_ether': str(transaction_fee_ether),
        'transaction_fee_dollar': str(transaction_fee_dollar)}),
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
