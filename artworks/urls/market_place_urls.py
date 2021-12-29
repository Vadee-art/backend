from django.urls import path
from artworks.views import market_place_views as views

urlpatterns = [
    path('', views.fetch_market_place, name='fetch_market_place'),
    path('deploy/', views.deploy_market_place, name='deploy_market_place'),
    path('fees/<str:pk>', views.fetch_transaction_fee, name='market_place_fees'),
]
