from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from artworks.serializer import ArtworkSerializer, OriginSerializer
from django.contrib.auth.models import User
from artworks.models import Artwork, Artist, Category, MyUser, Origin, SubCategory
from rest_framework import status
from artworks.serializer import CategorySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.http import HttpResponse
import json

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
def fetchOriginList(request):
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
        p = Paginator(artworks, 8)

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
def fetchTheArtWork(request, pk):
    artwork = Artwork.objects.get(_id=pk)
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@ api_view(['POST'])
@ permission_classes([IsAdminUser])
def createTheArtWork(request):
    user = request.user
    artist = Artist.objects.first()
    if user and artist:
        artwork = Artwork.objects.create(
            created_by=user,
            artist=artist,
            title='Default Title',
            subtitle='Default Subitle',
            about_work='empty!',
            provenance='empty!',
            width=0,
            height=0,
            depth=0,
            price=0,
        )
        serializer = ArtworkSerializer(artwork, many=False)
        return Response(serializer.data)
    else:
        return Response('هیچ هنرمندی وچود ندارد')


@ api_view(['PUT'])
@ permission_classes([IsAdminUser])
def updateTheArtwork(request, pk):
    data = request.data
    artwork = Artwork.objects.get(_id=pk)
    artist = Artist.objects.get(_id=data['artist'])
    created_by = MyUser.objects.get(_id=data['created_by'])
    artwork.created_by = created_by
    artwork.artist = artist
    artwork.title = data['title']
    artwork.subtitle = data['subtitle']
    artwork.year = data['year']
    artwork.category = data['category']
    artwork.medium = data['medium']
    artwork.condition = data['condition']
    artwork.classifications = data['classifications']
    artwork.width = data['width']
    artwork.height = data['height']
    artwork.depth = data['depth']
    artwork.unit = data['unit']
    artwork.isAnEdition = data['isAnEdition']
    artwork.editionNum = data['editionNum']
    artwork.editionSize = data['editionSize']
    artwork.is_signed = data['is_signed']
    artwork.is_authenticated = data['is_authenticated']
    artwork.frame = data['frame']
    artwork.isPrice = data['isPrice']
    artwork.price = data['price']
    artwork.about_work = data['about_work']
    artwork.provenance = data['provenance']
    artwork.art_location = data['art_location']
    artwork.quantity = data['quantity']

    artwork.save()
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@ api_view(['DELETE'])
@ permission_classes([IsAdminUser])
def deleteTheArtwork(request):
    data = request.data
    selectedArtworks = data['selectedArtworks']
    for _id in selectedArtworks:
        artworkDeleting = Artwork.objects.get(_id=_id)
        artworkDeleting.delete()
    return Response('artworks were deleted')


@ api_view(['POST'])
# @permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data
    artwork_id = data['artworkId']
    artwork = Artwork.objects.get(_id=artwork_id)

    artwork.image = request.FILES.get('image')
    artwork.save()
    return Response('عکس شما در دیتابیس ذخیره شد')
