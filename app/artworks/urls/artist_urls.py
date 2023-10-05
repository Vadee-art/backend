from artworks.views import artist_views as views
from django.urls import include, path
from rest_framework import routers

app_name = "artist"

router = routers.DefaultRouter()
router.register(r'', views.ArtistsView, basename='Artist')


urlpatterns = [
    path('', include(router.urls)),
    path("search/", views.ArtistSearch.as_view(), name="artists-search"),
    path(
        "<int:artistId>/related-artworks/",
        views.ArtistRelatedArtworks.as_view(),
    ),
    path(
        "<int:artistId>/similar/",
        views.ArtistSimilarArtists.as_view(),
    ),
    path(
        "filters",
        views.ArtistFiltersView.as_view(),
    ),
    # path(
    #     "<int:pk>/gallery/update/",
    #     views.update_artist_gallery,
    #     name="artist_gallery_update",
    # ),
]
