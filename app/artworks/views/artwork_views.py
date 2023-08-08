from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from artworks.serializer import (
    ArtworkSerializer,
    OrderSerializer,
    OriginSerializer,
    TheTokenSerializer,
    VoucherSerializer,
)
from django.contrib.auth.models import User
from artworks.models import (
    Artwork,
    Artist,
    Category,
    MyUser,
    Order,
    Origin,
    ShippingAddress,
    SubCategory,
    TheMarketPlace,
    TheToken,
    Voucher,
)
from rest_framework import status
from artworks.serializer import CategorySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from django.http import HttpResponse
import json
from rest_framework import filters, generics, viewsets, mixins

# for admin and change_form.html


@api_view(["GET"])
def get_subcategory(request):
    id = request.GET.get("id", "")
    result = list(SubCategory.objects.filter(category_id=int(id)).values("_id", "name"))
    return HttpResponse(json.dumps(result), content_type="application/json")


@api_view(["GET"])
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(["GET"])
def fetch_origin_list(request):
    origins = Origin.objects.all()
    list = []
    for o in origins:
        artworks = o.artwork_set.all()
        originSerializer = OriginSerializer(o, many=False)
        artworkSerializer = ArtworkSerializer(artworks, many=True)
        list.append(
            {"origin": originSerializer.data, "artworks": artworkSerializer.data}
        )

    return Response(list)


class ArtworkViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = (
        Artwork.objects.select_related(
            'artist', 'collection', 'category', 'origin', 'sub_category', 'voucher'
        )
        .prefetch_related('tags')
        .all()
    )
    serializer_class = ArtworkSerializer
    ordering_fields = ['-created_at']
    ordering = ['-created_at']


class CarouselArtworkViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = (
        Artwork.objects.filter(is_carousel=True)
        .select_related(
            'artist', 'collection', 'category', 'origin', 'sub_category', 'voucher'
        )
        .prefetch_related('tags')
        .all()
    )
    serializer_class = ArtworkSerializer
    ordering_fields = ['-created_at']
    ordering = ['-created_at']


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_the_artwork(request, pk, action):
    user = request.user
    data = request.data
    artwork = Artwork.objects.get(_id=pk)

    # 1 - Action Sign: update product when sign the product
    if user and action == "Signing":
        voucher = Voucher.objects.create(
            title=data["title"],
            artwork_id=int(data["artworkId"]),
            edition_number=data["editionNumber"],
            edition=data["edition"],
            price_wei=data["priceWei"],
            price_dollar=data["priceDollar"],
            token_Uri=data["tokenUri"],
            content=data["content"],
            signature=data["signature"],
        )
        voucher.save()

        artwork.owner = user
        artwork.voucher = voucher
        artwork.on_market = True
        artwork.is_minted = False
        artwork.save()
        serializer = VoucherSerializer(voucher, many=False)
        return Response({"voucher": serializer.data})

    # 2 - Action Redeem and Mint: update product when mint the product
    elif user and action == "RedeemAndMint":
        # a - create NFT
        token = TheToken.objects.create(
            market_item_id=None,
            token_id=data["tokenId"],
            contract=data["galleryAddress"],
        )
        token.artwork = artwork
        token.holder = user
        token.save()

        # b - create order
        order = Order.objects.create(
            transaction_hash=data["transactionHash"],
            price_eth=data["priceEth"],
            fee_eth=data["feeEth"],
        )
        order.seller = artwork.owner
        order.buyer = user
        order.is_delivered = False
        order.save()

        # c - relate the shipping address and order
        shipping_address = ShippingAddress.objects.create(
            address=data["address"],
            postal_code=data["postalCode"],
            city=data["city"],
            province=data["province"],
            country=data["country"],
            phone=data["phoneNumber"],
        )
        shipping_address.order = order
        shipping_address.buyer = user
        shipping_address.save()

        if artwork.edition_number < artwork.edition_total:
            artwork.edition_number += 1

        if artwork.edition_number == artwork.edition_total:
            artwork.is_sold_out = True

        # artwork.owner = user
        artwork.on_market = False
        artwork.is_minted = True
        artwork.save()

        # delete the voucher and update artwork
        voucher = artwork.voucher
        voucher.delete()

        serializer = OrderSerializer(order, many=False)
        return Response({"order": serializer.data})


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_the_artwork(request):
    data = request.data
    selectedArtworks = data["selectedArtworks"]
    for _id in selectedArtworks:
        artworkDeleting = Artwork.objects.get(_id=_id)
        artworkDeleting.delete()
    return Response("artworks were deleted")


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_the_voucher(request, pk):
    voucher = Voucher.objects.get(_id=pk)
    # voucher artwork id --> artworkId , editionNumber --> 73
    # e.i 73 ---> x = [ 7, 3]
    x = [int(a) for a in str(voucher.artwork_id)]
    artworkId = x[0]
    artwork = Artwork.objects.get(_id=artworkId)
    artwork.on_market = False
    artwork.save()

    voucher.delete()

    return Response("signature was deleted")


@api_view(["GET"])
def fetch_is_talent(request):
    artwork = Artwork.objects.filter(is_artist_talented=True).first()
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)
