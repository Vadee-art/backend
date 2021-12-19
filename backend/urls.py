"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# to use MEDIA_URL in setting
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routes/', include('artworks.urls.routes_urls')),
    path('api/v1/market/', include('artworks.urls.market_place_urls')),
    path('api/v1/artworks/', include('artworks.urls.artwork_urls')),
    path('api/v1/users/', include('artworks.urls.user_urls')),
    path('api/v1/artists/', include('artworks.urls.artist_urls')),
    path('api/v1/articles/', include('artworks.urls.article_urls')),
    path('api/v1/orders/', include('artworks.urls.order_urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
