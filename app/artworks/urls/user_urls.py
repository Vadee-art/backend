from artworks.views import user_views as views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('profile', views.UserProfile, basename='Profile')
router.register('profile-picture/', views.UserProfileImage, basename='ProfilePicture')

urlpatterns = [
    path('', include(router.urls)),
    path("login/", views.TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("login-web3/", views.Web3TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("register/", views.CreateUserView.as_view(), name="register"),
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
    path("artist/favorite/<int:pk>/", views.addFavoriteArtist, name="favorite_add_artist"),
    # path('update/<int:pk>/', views.updateUserById, name='user_update_by_id'),
    path("", views.fetchUsers, name="users"),
    path("delete/", views.deleteUser, name="user_delete"),
    path("<int:pk>/", views.fetchUsersById, name="user_by_id"),
]
