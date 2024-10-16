from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderPagination(PageNumberPagination):
    page_size = 2

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('product', 'order').all()
    serializer_class = OrderItemSerializer
