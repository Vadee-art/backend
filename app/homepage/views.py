from artworks.models import Artist, Artwork, Genre, Origin
from artworks.serializer import (
    ArtistSerializer,
    CategorySerializer,
    OriginSerializer,
    SimpleArtworkSerializer,
)
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView


class HomepageView(APIView):
    def get(self, request):
        artwork_query = Artwork.simple_object.select_related(
            'artist', 'artist__origin', 'artist__user'
        ).all()

        carousels = artwork_query.filter(is_carousel=True)[:5]
        artists = (
            Artist.objects.filter(is_featured=True)
            .annotate(art_count=Count("artworks"))
            .order_by("-art_count")
            .select_related("user")
            .prefetch_related("achievements", "favorites")[:6]
        )
        featured_categories = Genre.objects.filter(is_featured=True)[:5]
        last_artwork = artwork_query.order_by("-created_at").first()
        talented_artwork = artwork_query.filter(is_artist_talented=True).first()
        # sub_categories = SubCategory.objects.filter(is_featured=True).order_by("-created_at")[:5]
        origins = Origin.objects.filter(is_featured=True).order_by("_id")[:5]
        selected_categories = Genre.objects.filter(show_in_homepage=True)[:2]
        result = dict(
            carousels=SimpleArtworkSerializer(
                carousels, many=True, context={"request": request}
            ).data,
            artists=ArtistSerializer(artists, many=True, context={"request": request}).data,
            featuredCategories=CategorySerializer(
                featured_categories, many=True, context={"request": request}
            ).data,
            lastArtwork=SimpleArtworkSerializer(last_artwork, context={"request": request}).data,
            talentedArtwork=SimpleArtworkSerializer(
                talented_artwork, context={"request": request}
            ).data,
            # subCategories=SubCategorySerializer(
            #     sub_categories, many=True, context={"request": request}
            # ).data,
            origins=OriginSerializer(origins, many=True, context={"request": request}).data,
            selectedArtworks={
                genre.name: SimpleArtworkSerializer(
                    artwork_query.filter(genre=genre).order_by('-created_at')[:6],
                    many=True,
                    context={"request": request},
                ).data
                for genre in selected_categories
            },
        )
        return Response(data=result)
