from django.urls import path
from artworks.views import article_views as views


urlpatterns = [
    path('theArticle/', views.fetchTheArticle, name='theArticle'),
]
