from django.urls import path
from order.views import create_order

urlpatterns = [
    path('orders/', create_order, name='create-order'),
]
