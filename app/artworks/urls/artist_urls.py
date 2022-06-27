from django.urls import path
from artworks.views import artist_views as views

app_name = "artist"

urlpatterns = [
    path("", views.artist_list, name="artists"),
    path("search/", views.ArtistSearch.as_view(), name="artists-search"),
    path("talent/", views.fetch_is_talent, name="is_talent"),
    path("<int:pk>/", views.artist_by_id, name="artist_by_id"),
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
    path(
        "<int:pk>/gallery/update/",
        views.update_artist_gallery,
        name="artist_gallery_update",
    ),
]
