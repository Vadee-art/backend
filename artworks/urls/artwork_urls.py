from django.urls import path
from artworks.views import artwork_views as views


urlpatterns = [
    path('', views.fetchArtWorks, name='artWorks'),
    path('delete/', views.deleteTheArtwork, name='artwork-delete'),
    path('create/', views.createTheArtWork, name='image-create'),
    path('upload/', views.uploadImage, name='artwork-upload'),
    path('update/<int:pk>/', views.updateTheArtwork, name='artwork-update'),
    path('<int:pk>/', views.fetchTheArtWork, name='theArtWork'),
]
