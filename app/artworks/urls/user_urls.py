from django.urls import path
from artworks.views import user_views as views


urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("profile/me", views.UserProfile.as_view(), name="users-profile"),
    path("profile/update/", views.updateUserProfile, name="users-profile-update"),
    path("profile/artworks/mine", views.fetchMyArtworks, name="users-profile-artworks"),
    path(
        "profile/artworks/favorites/",
        views.fetchFavoriteArtworkList,
        name="favorite_artworks",
    ),
    path(
        "profile/artists/favorites/",
        views.fetchFavoriteArtistList,
        name="favorite_artists",
    ),
    path(
        "artwork/favorite/<int:pk>/",
        views.addFavoriteArtwork,
        name="favorite_add_artwork",
    ),
    path(
        "artist/favorite/<int:pk>/", views.addFavoriteArtist, name="favorite_add_artist"
    ),
    # path('update/<int:pk>/', views.updateUserById, name='user_update_by_id'),
    path("", views.fetchUsers, name="users"),
    path("delete/", views.deleteUser, name="user_delete"),
    path("<int:pk>/", views.fetchUsersById, name="user_by_id"),
]
