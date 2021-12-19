from django.urls import path
from artworks.views import user_views as views


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),
    path('store/update/', views.updateUserStore, name='users_store_update'),
    path('profile/', views.fetchUserProfile, name='users_profile'),
    path('profile/update/', views.updateUserProfile, name='users_profile_update'),
    path('profile/artworks/mine', views.fetchMyArtworks, name='users_profile_artworks'),
    path('profile/artworks/favorites/', views.fetchFavoriteArtworkList, name='favorite_artworks'),
    path('profile/artists/favorites/', views.fetchFavoriteArtistList, name='favorite_artists'),
    path('artwork/favorite/<int:pk>/', views.addFavoriteArtwork, name='favorite_add'),
    path('artist/favorite/<int:pk>/', views.addFavoriteArtwork, name='favorite_add'),
    # path('update/<int:pk>/', views.updateUserById, name='user_update_by_id'),
    path('', views.fetchUsers, name='users'),
    path('delete/', views.deleteUser, name='user_delete'),
    path('<int:pk>/', views.fetchUsersById, name='user_by_id'),
]
