from django.urls import path
from artworks.views import routes_views as views


urlpatterns = [
    path('', views.getRoutes, name='routes'),
]
