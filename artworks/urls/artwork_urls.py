from django.urls import path
from artworks.views import artwork_views as views


urlpatterns = [
    path('getSubcategory/', views.get_subcategory, name='sub_category_list'),
    path('categories/', views.categories, name='category_list'),
    path('', views.fetchArtworkList, name='artworks'),
    path('origins/', views.fetchOriginList, name='origins'),
    path('delete/', views.deleteTheArtwork, name='artwork-delete'),
    path('create/', views.createTheArtWork, name='image-create'),
    path('upload/', views.uploadImage, name='artwork-upload'),
    path('update/<int:pk>/', views.updateTheArtwork, name='artwork-update'),
    path('<int:pk>/', views.fetchTheArtWork, name='theArtWork'),
]
