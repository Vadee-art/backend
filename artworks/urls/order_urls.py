from django.urls import path
from artworks.views import order_views as views


urlpatterns = [
    path('', views.fetchOrders, name='orders'),
    path('add/', views.addOrderItems, name='add-orders'),
    path('myOrders/', views.fetchMyOrders, name='my-orders'),
    path('<str:pk>/deliver/', views.updateOrderToDelivered, name='order-deliver'),
    path('<str:pk>/', views.fetchOrderById, name='user-order_by_id'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='order-pay')
]
