from django.urls import path
from artworks.views import user_views as views


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.fetchUserProfile, name='users-profile'),
    path('profile/update/', views.updateUserProfile, name='users-profile-update'),
    path('update/<int:pk>/', views.updateUserById, name='user-update_by_id'),
    path('', views.fetchUsers, name='users'),
    path('delete/', views.deleteUser, name='user-delete'),
    path('<int:pk>/', views.fetchUsersById, name='user_by_id'),

]
