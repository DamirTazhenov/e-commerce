from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .tasks import send_order_confirmation_email, process_order
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product


class OrderPagination(PageNumberPagination):
    page_size = 2


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        total_amount = Decimal('0.00')

        # Check if there are any items in the order
        if 'items' not in data or not data['items']:
            return Response({'error': 'No items in the order'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=user, total_amount=0)

        # Loop through each item in the order data
        for item in data['items']:
            product = get_object_or_404(Product, id=item['product_id'])
            quantity = item['quantity']
            price = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

            total_amount += price

        order.total_amount = total_amount
        order.save()

        send_order_confirmation_email.delay(user.email, order.id)
        process_order.delay(order.id)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('product', 'order').all()
    serializer_class = OrderItemSerializer
