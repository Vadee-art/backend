from django.urls import path
from artworks.views import artist_views as views


urlpatterns = [
    path('', views.artist_list, name='artists'),
    path('<int:pk>/', views.artist_by_id, name='artist_by_id'),
    path('<int:pk>/gallery/update/', views.update_artist_gallery,
         name='artist_gallery_update'),

]
