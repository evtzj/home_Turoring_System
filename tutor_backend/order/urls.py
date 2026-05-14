from django.urls import path
from order.views import list_or_create_order,order_detail

urlpatterns = [
    path('orders/', list_or_create_order, name='create-order'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
]
