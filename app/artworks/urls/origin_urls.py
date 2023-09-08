from artworks.views import origin_views
from django.urls import include, path
from rest_framework import routers

app_name = "origins"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', origin_views.OriginViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
