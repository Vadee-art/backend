from artworks.models import Artist, Artwork, Category, Origin, SubCategory
from artworks.serializer import (
    ArtistSerializer,
    ArtworkSerializer,
    CategorySerializer,
    OriginSerializer,
    SimpleArtworkSerializer,
    SubCategorySerializer,
)
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView


class HomepageView(APIView):
    def get(self, request):
        artwork_query = Artwork.objects.select_related(
            'artist',
            'collection',
            'category',
            'origin',
            'sub_category',
            'artist__user',
            'owner',
        ).prefetch_related('tags', 'artist__achievements', 'artist__favorites')

        carousels = artwork_query.filter(is_carousel=True)[:5]
        artists = (
            Artist.objects.filter(is_featured=True)
            .annotate(art_count=Count("artworks"))
            .order_by("-art_count")
            .select_related("user")
            .prefetch_related("achievements", "favorites")[:6]
        )
        featured_categories = Category.objects.filter(is_featured=True)[:5]
        last_artwork = artwork_query.order_by("-created_at").first()
        talented_artwork = artwork_query.filter(is_artist_talented=True).first()
        sub_categories = SubCategory.objects.filter(is_featured=True).order_by("-created_at")[:5]
        origins = Origin.objects.filter(is_featured=True).order_by("_id")[:5]
        selected_categories = Category.objects.filter(show_in_homepage=True)[:2]
        result = dict(
            carousels=ArtworkSerializer(carousels, many=True, context={"request": request}).data,
            artists=ArtistSerializer(artists, many=True, context={"request": request}).data,
            featuredCategories=CategorySerializer(
                featured_categories, many=True, context={"request": request}
            ).data,
            lastArtwork=ArtworkSerializer(last_artwork, context={"request": request}).data,
            talentedArtwork=ArtworkSerializer(talented_artwork, context={"request": request}).data,
            subCategories=SubCategorySerializer(
                sub_categories, many=True, context={"request": request}
            ).data,
            origins=OriginSerializer(origins, many=True, context={"request": request}).data,
            selectedArtworks={
                category.name: SimpleArtworkSerializer(
                    Artwork.objects.filter(category=category).order_by('-created_at')[:6],
                    many=True,
                    context={"request": request},
                ).data
                for category in selected_categories
            },
        )
        return Response(data=result)
