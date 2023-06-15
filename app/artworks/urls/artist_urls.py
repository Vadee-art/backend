from django.urls import path, include

from artworks.views import artist_views as views
from rest_framework import routers

app_name = "artist"

router = routers.DefaultRouter()
router.register(r'', views.ArtistsView)

urlpatterns = [
    path('', include(router.urls)),
    path("search/", views.ArtistSearch.as_view(), name="artists-search"),
    path(
        "artist/related/<int:artistId>/",
        views.ArtistRelatedArtworks.as_view(),
        name="artist_related_artworks",
    ),
    path(
        "artist/similar/<int:artistId>/",
        views.ArtistSimilarArtists.as_view(),
        name="artist_related_artists",
    ),
    # path(
    #     "<int:pk>/gallery/update/",
    #     views.update_artist_gallery,
    #     name="artist_gallery_update",
    # ),
]
