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
# to use MEDIA_URL in setting
from cart.views import CartView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from homepage.views import HomepageView
from rest_framework import authentication, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title='Vadee API',
        default_version='v1',
    ),
    url=settings.DOMAIN,
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=(JWTAuthentication,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/homepage/", HomepageView.as_view()),
    path("api/v1/market/", include("artworks.urls.market_place_urls")),
    path("api/v1/artworks/", include("artworks.urls.artwork_urls")),
    path("api/v1/users/", include("artworks.urls.user_urls")),
    path("api/v1/artists/", include("artworks.urls.artist_urls")),
    path("api/v1/articles/", include("artworks.urls.article_urls")),
    path("api/v1/orders/", include("artworks.urls.order_urls")),
    path("api/v1/origins/", include("artworks.urls.origin_urls")),
    path("docs/", include_docs_urls(title="Vadee")),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    # Cart
    path("api/v1/cart/", CartView.as_view()),
    path('__debug__/', include('debug_toolbar.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
