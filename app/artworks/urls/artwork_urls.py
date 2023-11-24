from artworks.views import artwork_views as views
from django.urls import include, path
from rest_framework import routers

app_name = "artwork"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', views.ArtworkViewSet)
router.register(r'carousels/', views.CarouselArtworkViewSet)
router.register(r'by-origins/', views.OriginsArtworksView, basename='artworks_by_origin')
router.register(r'vouchers/', views.VoucherViewSet, basename='voucher')

urlpatterns = [
    path("talent/", views.fetch_is_talent, name="talent_artwork"),
    path("genres/", views.categories, name="category_list"),
    path('', include(router.urls)),
    path('filters/', views.ArtworkFiltersView.as_view()),
    path("delete/", views.delete_the_artwork, name="artwork_delete"),
    path("voucher/<int:pk>/delete/", views.delete_the_voucher, name="voucher_delete"),
    path("update/<int:pk>/<str:action>/", views.update_the_artwork, name="artwork_update"),
    path("<int:id>/similar/", views.SimilarArtworks.as_view()),
    path("<int:id>/save/", views.SaveArtwork.as_view()),
    path("<int:id>/unsave/", views.UnSaveArtwork.as_view()),
]
