from artworks.views import artwork_views as views
from django.urls import include, path
from rest_framework import routers

app_name = "artist"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', views.ArtworkViewSet)
router.register(r'carousels/', views.CarouselArtworkViewSet)

urlpatterns = [
    path("getSubcategory/", views.get_subcategory, name="sub_category_list"),
    path("talent/", views.fetch_is_talent, name="talent_artwork"),
    path("categories/", views.categories, name="category_list"),
    path('', include(router.urls)),
    path('filters/', views.ArtworkFiltersView.as_view()),
    path("origins/", views.fetch_origin_list, name="origins"),
    path("delete/", views.delete_the_artwork, name="artwork_delete"),
    path("voucher/<int:pk>/delete/", views.delete_the_voucher, name="voucher_delete"),
    path(
        "update/<int:pk>/<str:action>/", views.update_the_artwork, name="artwork_update"
    ),
]
