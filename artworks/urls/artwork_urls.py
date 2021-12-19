from django.urls import path
from artworks.views import artwork_views as views


urlpatterns = [
    path('getSubcategory/', views.get_subcategory, name='sub_category_list'),
    path('categories/', views.categories, name='category_list'),
    path('', views.fetchArtworkList, name='artworks'),
    path('origins/', views.fetch_origin_list, name='origins'),
    path('delete/', views.delete_the_artwork, name='artwork_delete'),
    path('create/', views.create_the_artwork, name='image_create'),
    path('upload/', views.upload_image, name='artwork_upload'),
    path('update/<int:pk>/<str:action>/',
         views.update_the_artwork, name='artwork_update'),
    path('<int:pk>/', views.fetch_the_artwork, name='the_artWork'),
]
