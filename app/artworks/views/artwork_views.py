from artworks.filters import ArtworkFilter
from artworks.models import (
    Artwork,
    Genre,
    Order,
    Origin,
    ShippingAddress,
    Technique,
    Theme,
    TheToken,
    Voucher,
)
from artworks.serializer import (
    ArtworkSerializer,
    GenreSerializer,
    OrderSerializer,
    OriginSerializer,
    OriginWithArtworksSerializer,
    SimpleArtworkSerializer,
    TechniqueSerializer,
    ThemeSerializer,
    VoucherSerializer,
)
from django.db.models import F, Window
from django.db.models.functions import Rank
from django.shortcuts import get_object_or_404
from django_cte import With
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
def categories(request):
    categories = Genre.objects.all()
    serializer = GenreSerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)


class SimilarArtworks(views.APIView):
    def get(self, request, id):
        artwork = get_object_or_404(Artwork, pk=id)
        result = SimpleArtworkSerializer(
            artwork.similar_artworks, many=True, context={"request": request}
        ).data
        return Response(data=result)


class SaveArtwork(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        artwork = get_object_or_404(Artwork.objects, pk=id)
        request.user.saved_artworks.add(artwork)
        return Response()


class UnSaveArtwork(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        artwork = get_object_or_404(Artwork.objects, pk=id)
        request.user.saved_artworks.remove(artwork)
        return Response()


class OriginsArtworksView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Origin.objects.order_by("_id")
    serializer_class = OriginWithArtworksSerializer

    def list(self, request):
        origins = self.paginate_queryset(self.queryset)
        cte = With(
            Artwork.objects.annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F("created_at").desc(),
                    partition_by=[F("artist__origin_id")],
                )
            )
        )
        artworks = (
            cte.queryset()
            .select_related(
                "artist__user",
                "artist__origin",
            )
            .with_cte(cte)
            .filter(artist__origin__in=origins)
            .annotate(rank=cte.col.rank)
            .filter(rank__lte=3)
        )
        q = str(artworks.query)
        print(q)

        for origin in origins:
            origin.artworks = [a for a in artworks if a.artist.origin_id == origin.pk]

        return self.get_paginated_response(
            data=OriginWithArtworksSerializer(origins, many=True, context={"request": request}).data
        )


class ArtworkViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    ordering_fields = ['-created_at']
    ordering = ['-created_at']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtworkFilter
    serializer_classes = {
        'retrieve': SimpleArtworkSerializer,
        'list': ArtworkSerializer,
    }

    default_serializer_class = ArtworkSerializer

    def get_queryset(self):
        if self.action == 'list':
            return (
                Artwork.objects.select_related(
                    'collection',
                    'artist',
                    'artist__user',
                    'artist__origin',
                    'genre',
                    'theme',
                    'technique',
                )
                .prefetch_related(
                    'tags',
                )
                .all()
            )
        return Artwork.objects.all()


class ArtworkFiltersView(views.APIView):
    def get(self, request):
        genres = Genre.objects.order_by("-created_at")
        themes = Theme.objects.order_by("-created_at")
        techniques = Technique.objects.order_by("-created_at")
        origins = Origin.objects.order_by("_id")

        result = dict(
            origins=OriginSerializer(origins, many=True, context={"request": request}).data,
            themes=ThemeSerializer(themes, many=True, context={"request": request}).data,
            techniques=TechniqueSerializer(
                techniques, many=True, context={"request": request}
            ).data,
            genres=GenreSerializer(genres, many=True, context={"request": request}).data,
        )
        return Response(data=result)


class CarouselArtworkViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Artwork.objects.filter(is_carousel=True).all()
    serializer_class = ArtworkSerializer
    ordering_fields = ['-created_at']
    ordering = ['-created_at']


class VoucherViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    ordering_fields = ['-created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        self.validate()
        return super().perform_create(serializer)

    def perform_destroy(self, serializer):
        self.validate()
        return super().perform_destroy(serializer)

    def perform_update(self, serializer):
        self.validate()
        return super().perform_update(serializer)

    def validate(self):
        artwork = Artwork.objects.filter(pk=self.request.data['artwork_id']).first()
        if not artwork or self.request.user != artwork.artist.user:
            raise ValidationError('Artwork not found')


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
