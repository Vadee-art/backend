from django.urls import path, include
from artworks.views import artwork_views as views

from rest_framework import routers

app_name = "artist"

router = routers.DefaultRouter()
router.register(r'', views.ArtworkViewSet)


urlpatterns = [
    path("getSubcategory/", views.get_subcategory, name="sub_category_list"),
    path("talent/", views.fetch_is_talent, name="talent_artwork"),
    path("categories/", views.categories, name="category_list"),
    path('', include(router.urls)),
    path("carousels/", views.fetch_is_carousel, name="carousels"),
    path("origins/", views.fetch_origin_list, name="origins"),
    path("delete/", views.delete_the_artwork, name="artwork_delete"),
    path("voucher/<int:pk>/delete/", views.delete_the_voucher, name="voucher_delete"),
    path(
        "update/<int:pk>/<str:action>/", views.update_the_artwork, name="artwork_update"
    ),
    path("<int:pk>/", views.fetch_the_artwork, name="the_artWork"),
]
