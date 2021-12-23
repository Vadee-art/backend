from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from artworks.serializer import ArtworkSerializer, OriginSerializer, VoucherSerializer
from django.contrib.auth.models import User
from artworks.models import Artwork, Artist, Category, MyUser, Origin, SubCategory, TheMarketPlace, Voucher
from rest_framework import status
from artworks.serializer import CategorySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.http import HttpResponse
import json
import requests

# for admin and change_form.html


@api_view(['GET'])
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(
        category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_origin_list(request):
    origins = Origin.objects.all()
    serializer = OriginSerializer(origins, many=True)
    return Response({'origins': serializer.data})


@api_view(['GET'])
def fetchArtworkList(request):
    query = request.query_params.get('keyword')
    page = request.query_params.get('page')
    query_region = request.query_params.get('regions')
    query_artist = request.query_params.get('artist')
    query_category = request.query_params.get('category')

    if query_category:
        category = Category.objects.get(id=query_category)
        artworks = Artwork.objects.filter(
            category=category).order_by('created_at')
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({'artworks': serializer.data})

    if query_artist:
        artist = Artist.objects.get(_id=query_artist)
        artworks = Artwork.objects.filter(
            artist=artist).order_by('created_at')
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({'artworks': serializer.data})

    elif query_region:
        origin = Origin.objects.filter(
            country__icontains=query_region).first()
        artworks = Artwork.objects.filter(
            origin=origin).order_by('created_at')
        serializer = ArtworkSerializer(artworks, many=True)
        return Response({'artworks': serializer.data})

    elif query == None:
        query = ''
        # we could use any value instead of title
        artworks = Artwork.objects.filter(
            title__icontains=query).order_by('created_at')
        # pagination
        p = Paginator(artworks, 10)

        try:
            artworks = p.page(page)
        except PageNotAnInteger:  # first render we have no page
            artworks = p.page(1)
        except EmptyPage:  # page does not exist return the last page
            artworks = p.page(p.num_pages)

        if page == None:
            page = 1

        page = int(page)

        serializer = ArtworkSerializer(artworks, many=True)
        return Response({'artworks': serializer.data, 'page': page, 'pages': p.num_pages})


@ api_view(['GET'])
def fetch_the_artwork(request, pk):
    artwork = Artwork.objects.get(_id=pk)
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_the_artwork(request, pk, action):
    user = request.user
    data = request.data
    artwork = Artwork.objects.get(_id=pk)

    # 1 - Action Sign: update product when sign the product
    if user and action == 'Signing':
        voucher = Voucher.objects.create(
            title=data['title'],
            artwork_id=int(data['artworkId']),
            price=data['sellingPrice'],
            token_Uri=data['tokenUri'],
            content=data['content'],
            signature=data['signature']
        )
        voucher.save()

        artwork.voucher = voucher
        artwork.price_eth = data['sellingPrice']
        artwork.signer_address = data['sellerAddress']
        artwork.on_market = True
        artwork.save()
        serializer = VoucherSerializer(voucher, many=False)
        return Response({'voucher': serializer.data})


@ api_view(['DELETE'])
@ permission_classes([IsAdminUser])
def delete_the_artwork(request):
    data = request.data
    selectedArtworks = data['selectedArtworks']
    for _id in selectedArtworks:
        artworkDeleting = Artwork.objects.get(_id=_id)
        artworkDeleting.delete()
    return Response('artworks were deleted')
