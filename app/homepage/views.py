from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from artworks.models import Artist, Artwork, Category, Origin, SubCategory
from artworks.serializer import (
    ArtistSerializer,
    ArtworkSerializer,
    CategorySerializer,
    OriginSerializer,
    SubCategorySerializer,
)


class HomepageView(APIView):
    def get(self, request):
        artwork_query = Artwork.objects.select_related(
            "collection",
            "category",
            "origin",
            "sub_category",
            "voucher",
            "artist__user",
        ).prefetch_related("tags")

        carousels = artwork_query.filter(is_carousel=True)[:5]
        artists = (
            Artist.objects.annotate(art_count=Count("artwork_artist"))
            .order_by("-art_count")
            .select_related("user")
            .prefetch_related("achievements", "favorites")[:6]
        )
        featured_categories = Category.objects.filter(is_featured=True)[:5]
        last_artwork = artwork_query.order_by("-created_at").first()
        talented_artwork = artwork_query.filter(is_artist_talented=True).first()
        sub_categories = SubCategory.objects.order_by("-created_at")[:5]
        origins = Origin.objects.order_by("_id")[:5]

        result = dict(
            carousels=ArtworkSerializer(
                carousels, many=True, context={"request": request}
            ).data,
            artists=ArtistSerializer(
                artists, many=True, context={"request": request}
            ).data,
            featuredCategories=CategorySerializer(
                featured_categories, many=True, context={"request": request}
            ).data,
            lastArtwork=ArtworkSerializer(
                last_artwork, context={"request": request}
            ).data,
            talentedArtwork=ArtworkSerializer(
                talented_artwork, context={"request": request}
            ).data,
            subCategories=SubCategorySerializer(
                sub_categories, many=True, context={"request": request}
            ).data,
            origins=OriginSerializer(
                origins, many=True, context={"request": request}
            ).data,
        )
        return Response(data=result)
