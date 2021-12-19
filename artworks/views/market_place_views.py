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
@permission_classes([IsAuthenticated])
def fetch_market_place(request):
    market_place = TheMarketPlace.objects.first()
    serializer = MarketPlaceSerializer(market_place, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_transaction_fee(request, price):
    response = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=cad')
    data = response.json()
    ether_price = data['ethereum']['cad']
    market_place = TheMarketPlace.objects.first()
    oneL_fee_allocation = market_place.oneL_fee_allocation
    flu_fee_allocation = market_place.flu_fee_allocation
    chain_fee_allocation = market_place.chain_fee_allocation

    transaction_fee_ether = market_place.fetch_transaction_fee(float(price))

    transaction_fee_dollar = market_place.fetch_transaction_fee(
        float(int(data['ethereum']['cad']) * float(price)))

    return HttpResponse(json.dumps({
        'transaction_fee_ether': str(transaction_fee_ether),
        'transaction_fee_dollar': str(transaction_fee_dollar),
        'oneL_fee_allocation': str(oneL_fee_allocation),
        'flu_fee_allocation': str(flu_fee_allocation),
        'chain_transactchain_fee': str(chain_fee_allocation)}), content_type="application/json")


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
